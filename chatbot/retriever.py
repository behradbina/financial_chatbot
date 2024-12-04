import os 
import re
import heapq
import uuid

import torch
import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun


class Retriever(BaseRetriever):
    ip_address: str = os.getenv('IP_ADDRESS')
    username: str = os.getenv('USER_NAME')
    password: str = os.getenv('PASSWORD')
    chunk_size: int = int(os.getenv('CHUNK_SIZE', 1000))
    chunk_overlap: int = int(os.getenv('CHUNK_OVERLAP', 100))
    documents_path: str = os.getenv('DOCUMENT_PATH', './data/finance_department.xlsx')
    index_name: str = os.getenv('INDEX_NAME', 'isc_financial')
    stop_words_path:str = os.getenv('STOP_WORDS_PATH', './StopWords/Persian_Stop_Words.txt')
    top_k: int = int(os.getenv('TOP_K', 7))
    embedding_model: SentenceTransformer = None
    es: Elasticsearch = None
    stop_words: set = None
    documents: list = None
    _instance = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.embedding_model = self.__init_embedding_model(os.getenv('EMBEDDING_MODEL_PATH', './SentenceTransformer'))
        self.es = None
        with open(self.stop_words_path, "r", encoding="utf-8-sig") as file:
            self.stop_words = set(line.strip() for line in file)
            
        self.__connection()
        
        if not self.es.indices.exists(index=self.index_name):
            self.documents = self.__load_documents(self.documents_path)
            self.__create_index()
            self.insert_new_data(self.documents)
        else:
            print("index allready exist!")
        
    def __connection(self):
        if self.es is not None:
            return
        
        self.es = Elasticsearch(
            [self.ip_address],
            basic_auth=(self.username, self.password),
            verify_certs=False,
            ssl_show_warn=False
            )
        
        if self.es.ping():
            print("=" * 100)
            print("ElasticSearch Connection Status:")
            print(f"\t IP address: {self.ip_address}")
            print(f"\t Elasticsearch info: {self.es.info()}")
            print("=" * 100)
        else:
            raise ValueError(f"Failed to connect, please check the IP address and port number and try again")

    def clean_text(self, text):
        text = text.replace('\u200c', ' ')
        pattern = re.compile(r'[^\u0600-\u06FF0-9\s]+|[^\w\s]+')
        text = re.sub(pattern, '', text)
        text = ' '.join([word for word in text.split() if word not in self.stop_words])
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def __load_documents(self, filepath):
        """Load and clean documents from a CSV file"""
        data = pd.read_excel(filepath, header=None)[0]
        print("--------------------- Documents successfully loaded ---------------------")
        return data.tolist()
    
    def __create_index(self):
        index_config = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "persian_custom_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "char_filter": ["persian_char_filter"],
                            "filter": [
                                "lowercase",
                                "persian_normalization",
                                "persian_stop"
                            ]
                        }
                    },
                    "char_filter": {
                        "persian_char_filter": {
                            "type": "mapping",
                            "mappings": [
                                "آ => ا",
                                "ة => ه",
                                "ي => ی",
                                "ك => ک"
                            ]
                        }
                    },
                    "filter": {
                        "persian_normalization": {
                            "type": "persian_normalization"
                        },
                        "persian_stop": {
                            "type": "stop",
                            "stopwords": "_persian_"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "content": {
                        "type": "text"
                        },
                    "clean_content": {
                        "type": "text",
                        "analyzer": "persian_custom_analyzer",
                        "search_analyzer": "persian_custom_analyzer"
                        },
                    "embedding": {
                        "type": "dense_vector",
                        "dims": 1024,
                        "similarity": "l2_norm",
                        },
                }
            }
        }
        
        try:
            self.es.indices.create(index=self.index_name, body=index_config)
            print(f"--------------------- Index {self.index_name} created successfully ---------------------")
        except Exception as e:
            print("--------------------- Can't create index >>> ", e)
        

    def __init_embedding_model(self, embedding_model_path):
        """Initialize the embedding model"""
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = SentenceTransformer(embedding_model_path, local_files_only=True).to(device)
        model.eval()
        
        print("--------------------- Sentence embedding model successfully loaded ---------------------")
        return model
    
    def insert_new_data(self, documents):
        
        print("--------------------- inserting new data using Agenitc Chunking ...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        
        if isinstance(documents, list):
            chunked_documents = text_splitter.split_documents([Document(page_content=text) for text in documents])

        if isinstance(documents, str):
            documents = [Document(page_content=documents)]
            chunked_documents = text_splitter.split_documents(documents)    

        actions = []
        
        for i, doc in enumerate(chunked_documents):
            print(f'[{i} / {len(chunked_documents)}]')
            embedding = self.embedding_model.encode(doc.page_content, convert_to_numpy=True)
            embedding = embedding / np.linalg.norm(embedding)
            
            doc_body = {
                "content": doc.page_content,
                "clean_content": self.clean_text(doc.page_content), 
                "embedding": embedding.tolist()
            }
            actions.append({
                "_index": self.index_name,
                "_id": str(uuid.uuid4()),
                "_source": doc_body
                })
        if actions:
            print("---- Inserting data Using Bulk")
            helpers.bulk(self.es, actions, refresh='wait_for')       
        print("---------------------KnowledgeBase successfully created ---------------------")
        
    def reciprocal_rank_fusion(self, vector_results, text_results, k=60):
        scores = {}
        contents = {}
        
        for rank, hit in enumerate(text_results):
            doc_id = hit['_id']
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
            contents[doc_id] = hit['_source']['content']

        for rank, hit in enumerate(vector_results):
            doc_id = hit['_id']
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
            contents[doc_id] = hit['_source']['content']

        ranked_docs = heapq.nlargest(10, scores.items(), key=lambda x: x[1])
        ranked_content = []
        for doc_id, score in ranked_docs:
            if doc_id in contents:
                ranked_content.append(contents[doc_id])
        return ranked_content
    
    def _get_relevant_documents(self, query, *, run_manager: CallbackManagerForRetrieverRun):
        # ======================================= Full-text Search
        clean_question = self.clean_text(query)
        
        text_search_query = {
            "size": self.top_k,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "clean_content": {
                                    "query": clean_question,
                                    "fuzziness": "AUTO",
                                    "boost": 2.0
                                }
                            }
                        },
                        {
                            "match_phrase": {
                                "clean_content": {
                                    "query": clean_question,
                                    "slop": 3,
                                    "boost": 1.0
                                }
                            }
                        }
                    ],
                    "minimum_should_match": 1
                }
            }
        }
        text_results = self.es.search(index=self.index_name, body=text_search_query)['hits']['hits']
        
        # ======================================= Vector Search
        question_embedding = self.embedding_model.encode(query, convert_to_numpy=True)
        question_embedding = question_embedding / np.linalg.norm(question_embedding)
        
        vector_search_query = {
            "size": self.top_k,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0", 
                        "params": {"query_vector": question_embedding.tolist()}
                    }
                }
            }
        }
        vector_results = self.es.search(index=self.index_name, body=vector_search_query)['hits']['hits']
        
        combined_results = self.reciprocal_rank_fusion(vector_results, text_results, k=60)[:self.top_k]
        final_results = [Document(page_content=text) for text in combined_results]
        
        return final_results
    
    def drop_index(self):
        try:
            self.es.indices.delete(index=self.index_name)
            print(f"Index {self.index_name} deleted successfully.")
        except Exception as e:
            print(f"Can't Drop {self.index_name}: ", e)