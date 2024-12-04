import os
import pickle
from typing import List

import redis

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
#from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from langfuse.callback import CallbackHandler

from .retriever import Retriever


redis_client = redis.Redis(host='localhost', port=6379, db=0)
hybrid_search = Retriever()

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""شما یک مدل دستیار هوش مصنوعی هستید. وظیفه شما تولید 3 نسخه جایگزین 
    از سوال کاربر ارائه‌شده است، به طوری که کلمات کلیدی را با کلمات هم معنی جایگزین شود. 
    هیچ زمینه یا جزئیات اضافی اضافه نکنید. این سوالات جایگزین را با خطوط جدید از هم جدا کنید.
    سوال اصلی: {question}"""
)

PROMPT = PromptTemplate(
    input_variables=["question", "context"],
    template="""
    شما یک کارمند هوشمند بخش مالی شرکت خدمات انفورماتیک هستید. بر اساس قوانین و سوال مشتری، پاسخی 
    .واضح، کامل و با ساختار مناسب به زبان فارسی به صورت خیلی دوستانه ارائه دهید که تمام اطلاعات مرتبط برای پاسخ به سوال را شامل شود.
    اگر سوال به حوزه مالی مرتبط نبود یا ارتباط معناداری با قوانین نداشت، خودت یه پاسخ مناسب تولید کن. \n
    سوال: {question}\n
    قوانین:\n{context}"""
)

class LineListOutputParser(BaseOutputParser[List[str]]):
    def parse(self, text: str) -> List[str]:
        lines = text.strip().split("\n")
        return list(filter(None, lines))

class RAGModel:
    _instance = None  

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RAGModel, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self.ttl = int(os.getenv('TTL', 86400))
        self.k = int(os.getenv('K', 5))
        self.genrator_model = OllamaLLM(model=os.getenv('GENRATOR_MODEL_NAME', 'gemma2'))
        self.output_parser = LineListOutputParser()
        self.langfuse_handler = CallbackHandler(
            secret_key=os.getenv('LANGFUSE_SECRET_KEY'),
            public_key=os.getenv('LANGFUSE_PUBLIC_KEY'),
            host=os.getenv('LANGFUSE_HOST'),
        )
        self._initialized = True

    def get_user_memory(self, user_id):
        memory_data = redis_client.get(user_id)
        if memory_data:
            memory = pickle.loads(memory_data)
        else:
            memory = ConversationBufferWindowMemory(k=self.k)
        return memory
    
    def save_user_memory(self, user_id, memory):
        memory_data = pickle.dumps(memory)
        redis_client.setex(user_id, self.ttl, memory_data)

    def run_rag(self, query, user_id):        
        print(f"\n -------- Get User Chat Memory {user_id} ...")
        memory = self.get_user_memory(user_id)
        
        # Generating Alternative Queries
        retriever_chain = QUERY_PROMPT | self.genrator_model | self.output_parser
        
        # Aggregating Results from Alternative Queries
        multi_query_retriever = MultiQueryRetriever(
            retriever=hybrid_search, 
            llm_chain=retriever_chain, 
            parser_key="lines"
        )
        # Createing Answer Using LLM
        rag_chain = RetrievalQA.from_chain_type(
            llm=self.genrator_model,
            chain_type="stuff",
            memory=memory,
            retriever=multi_query_retriever,
            chain_type_kwargs={"prompt": PROMPT},
        )
        response = rag_chain.invoke(
            query, 
            config={
                "callbacks": [self.langfuse_handler],
            }
        )
        self.save_user_memory(user_id, memory)
        
        print('\n\n ==================== RAG response >>> ')
        print(response)
        
        return response["result"]