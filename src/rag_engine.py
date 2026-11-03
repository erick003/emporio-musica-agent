import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

VECTOR_STORE_DIR = "chroma_db"

def setup_rag_engine(pdf_path: str = "data/politicas_da_loja.pdf"):
    """Indexa o PDF de políticas no banco vetorial Chroma."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    if os.path.exists(VECTOR_STORE_DIR):
        vectorstore = Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings)
        return vectorstore.as_retriever(search_kwargs={"k": 3})
    
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(documents)
    
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=VECTOR_STORE_DIR
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def query_policies(query: str) -> str:
    """Consulta as políticas da loja via RAG."""
    retriever = setup_rag_engine()
    docs = retriever.invoke(query)
    if not docs:
        return "No specific store policy found regarding this topic."
    return "\n\n".join([d.page_content for d in docs])