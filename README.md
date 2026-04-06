# 🤖 RAG Document Chatbot

An intelligent document Q&A system powered by **Retrieval-Augmented Generation (RAG)**. Upload any PDF and have a natural conversation with its contents.

Built with LangChain, Groq (Llama 3.3-70b), HuggingFace Embeddings, and Streamlit.

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **PDF Upload & Processing** | Upload any PDF — the system extracts, chunks, and indexes it automatically |
| 🔍 **Multi-Query Retrieval** | User questions are rewritten into 3 optimized search queries for broader retrieval |
| 🧠 **Intelligent Chunking** | Documents split using RecursiveCharacterTextSplitter with overlap to preserve context |
| 💬 **Conversational Memory** | Sliding window memory with LLM-based summarization of older messages |
| 📊 **Answer Evaluation** | LLM-as-Judge scoring for faithfulness and relevancy on every response |
| 📚 **Source Attribution** | See exactly which document chunks informed the answer, with relevance scores |
| ⚡ **Streaming Responses** | Answers stream in real-time, token by token |

## 🏗️ Architecture

```
User uploads PDF
    ↓
PyPDFLoader extracts text
    ↓
RecursiveCharacterTextSplitter → ~800 char chunks with 100 char overlap
    ↓
HuggingFace (all-MiniLM-L6-v2) → 384-dim embeddings
    ↓
SKLearnVectorStore stores vectors
    ↓
User asks a question
    ↓
LLM Call #1: Query rewriting → 3 optimized search queries
    ↓
Multi-query similarity search → Top 5 unique chunks (deduplicated)
    ↓
LLM Call #2: Answer generation with context + conversation history
    ↓
LLM Call #3: Evaluation (faithfulness & relevancy scoring)
    ↓
Streamed answer + sources + evaluation displayed to user
```

## 🛠️ Tech Stack

- **LLM**: Llama 3.3-70b via Groq API
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (384-dim, runs locally)
- **Vector Store**: SKLearnVectorStore
- **Framework**: LangChain
- **Frontend**: Streamlit
- **Memory**: Custom sliding window + LLM summarization

## 📁 Project Structure

```
├── app.py                    # Main Streamlit entry point
├── pages/
│   └── chatbot.py            # Chat interface (orchestrates the full pipeline)
├── src/
│   ├── load_file.py          # PDF loading (uploaded or default)
│   ├── text_splitter.py      # Document chunking with RecursiveCharacterTextSplitter
│   ├── retriever.py          # Embedding creation & multi-query similarity search
│   ├── rewrite_query.py      # LLM-based query rewriting (3 queries per question)
│   ├── generator.py          # Answer generation with streaming & prompt engineering
│   ├── evaluator.py          # LLM-as-Judge evaluation (faithfulness & relevancy)
│   ├── memory.py             # Sliding window + summarization memory management
│   └── session_state.py      # Streamlit session state initialization
├── .streamlit/
│   └── config.toml           # Streamlit theme configuration
├── requirements.txt          # Python dependencies
└── .env                      # API keys (not committed)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Groq API key ([get one free](https://console.groq.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/summer0212/rag-document-chatbot.git
cd rag-document-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo 'GROQ_API_KEY="your_groq_api_key_here"' > .env

# Run the app
streamlit run app.py
```

### Usage
1. Open `http://localhost:8501` in your browser
2. Navigate to the **Chatbot** page from the sidebar
3. (Optional) Upload your own PDF using the sidebar uploader
4. Ask questions about the document!

## 🔑 Key Design Decisions

| Decision | Rationale |
|---|---|
| **800 char chunks, 100 overlap** | Balances embedding focus vs context preservation |
| **Multi-query (3 queries)** | Broader retrieval coverage than single-query search |
| **Sliding window memory (6 msgs)** | Prevents token overflow while retaining context via summarization |
| **LLM-as-Judge evaluation** | Real-time quality monitoring without manual ground truth |
| **Temperature=0 for evaluation** | Deterministic, reproducible scoring |

## 📈 Future Improvements

- [ ] Replace SKLearnVectorStore with ChromaDB/Pinecone for persistence
- [ ] Add support for multiple document formats (DOCX, TXT, HTML)
- [ ] Implement token-based truncation for more precise context management
- [ ] Add RAGAS framework for comprehensive evaluation with ground truth
- [ ] Deploy to Streamlit Cloud for public access

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
