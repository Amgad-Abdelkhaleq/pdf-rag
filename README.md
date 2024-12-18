# PDF Chatbot - AI-Powered Document Q&A

## Overview
A sophisticated AI chatbot that enables users to upload PDF documents and interact with them through an intelligent conversational interface.

## Features
- PDF document upload and text extraction
- Advanced Retrieval Augmented Generation (RAG)
- In-memory chat history management
- Modular and extensible architecture
- Docker containerization

## Setup Instructions

### Prerequisites
- Python 3.10+
- Docker (optional)

### Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application
#### Local Development
```bash
# Start FastAPI Backend
python main.py

# In another terminal, start Streamlit UI
streamlit run src/ui/streamlit_app.py
```

#### Docker Deployment
```bash
docker build -t pdf-chatbot .
docker run -p 8000:8000 -p 8501:8501 pdf-chatbot
```

## Architecture
- FastAPI Backend
- Streamlit Frontend
- Mistral LLM
- Hugging Face Embeddings
- Qdrant Vector Store

## Technologies
- FastAPI
- Streamlit
- Hugging Face Transformers
- Langchain
- Qdrant
- Ragas

## Testing
```bash
pytest tests/
```