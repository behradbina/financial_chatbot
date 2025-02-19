# Financial Department RAG-based QA System

This project is an AI-powered Retrieval-Augmented Generation (RAG) system designed for the financial departmentn. It integrates **Elasticsearch**, **LangChain**, and **Ollama** to provide intelligent and structured responses to user queries.

---

## 🔹 Features
- **Hybrid Search:** Combines full-text search and vector search for accurate document retrieval.
- **Persian Language Support:** Uses a custom text cleaner and Elasticsearch analyzers for Persian processing.
- **Multi-Query Expansion:** Rewrites user queries to improve search accuracy.
- **Memory-based User Sessions:** Stores conversation history in Redis for context-aware answers.
- **Customizable Large Language Model (LLM):** Supports various Ollama models (default: `gemma2`).
- **Elasticsearch Dense Vector Storage:** Stores embeddings for efficient similarity search.

---

## 🛠 Tech Stack
- **Python** (Django-based backend)
- **LangChain** (for RAG framework)
- **Elasticsearch** (hybrid retrieval)
- **SentenceTransformers** (embedding model)
- **Ollama** (LLM)
- **Redis** (for conversation memory)

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/financial-rag.git
cd financial-rag
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
Create a `.env` file and set up the required variables:
```
IP_ADDRESS=localhost
USER_NAME=your_es_username
PASSWORD=your_es_password
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
DOCUMENT_PATH=./data/finance_department.xlsx
INDEX_NAME=isc_financial
STOP_WORDS_PATH=./StopWords/Persian_Stop_Words.txt
TOP_K=7
EMBEDDING_MODEL_PATH=./SentenceTransformer
GENRATOR_MODEL_NAME=gemma2
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_HOST=http://your-langfuse-host
TTL=86400
K=5
```

### 4️⃣ Run the Application
```sh
python manage.py runserver
```

---

## 📌 Project Structure
```
├── retriever.py       # Hybrid document retriever using Elasticsearch & SentenceTransformers
├── rag_model.py       # RAG-based response generator using LangChain & Ollama
├── .env               # Configuration file (ignored in Git)
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```

---

## 🔍 How It Works

### 1️⃣ Data Indexing
- The `Retriever` class loads Persian financial documents, cleans the text, and indexes them in **Elasticsearch**.
- Uses **custom analyzers** to normalize Persian text.

### 2️⃣ Query Processing
- User queries are **cleaned and expanded** using multi-query generation.
- Searches are performed using:
  - **Full-text search** (fuzzy matching, phrase queries)
  - **Vector search** (cosine similarity with dense vectors)

### 3️⃣ Response Generation
- Retrieved documents are passed to **Ollama LLM** for response generation.
- **Redis** stores conversation memory for better context-awareness.

---

## 📌 API Usage
You can send queries via an API (Django endpoint):
```sh
POST /api/query
Content-Type: application/json

{
  "user_id": "12345",
  "query": "قوانین پرداخت مالی شرکت چیست؟"
}
```

### 🔄 Example Response:
```json
{
  "result": "طبق قوانین مالی شرکت، پرداخت‌های مالی طبق بخشنامه شماره ۱۲۳..."
}
```

---

## 🏗 Future Improvements
- Fine-tuning the embedding model for better retrieval.
- Adding a web UI for user-friendly interaction.
- Supporting additional financial datasets.

---

## 📜 License
MIT License. Feel free to contribute!
```
