import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from app.llm import OllamaLLM
from app.data_processing import get_markdown_files
from app.config import load_environment

def setup_pipeline():
    # Load environment variables
    config = load_environment()
    repo_url = config['REPO_URL']
    embedding_model_name = config['EMBEDDING_MODEL']
    base_url = config['BASE_URL']
    model_name = config['MODEL_NAME']

    # Clone repository and process markdown files
    markdown_files = get_markdown_files(repo_url)
    documents = []
    for file_path in markdown_files:
        loader = TextLoader(file_path)
        documents.extend(loader.load())

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    # Generate embeddings
    embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vectorstore = FAISS.from_documents(chunks, embedding_model)

    # Create RAG pipeline
    retriever = vectorstore.as_retriever()
    llm = OllamaLLM(base_url=base_url, model_name=model_name)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
