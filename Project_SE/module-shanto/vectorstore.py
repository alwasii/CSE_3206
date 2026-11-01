import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from module_1.config import get_settings
from module_1.embeddings import get_embeddings, get_embedding_dimension

settings = get_settings()

_vectorstore = None


def ensure_index():
    if not settings.pinecone_api_key:
        raise RuntimeError("PINECONE_API_KEY is missing")

    desired_dimension = get_embedding_dimension()
    pc = Pinecone(api_key=settings.pinecone_api_key)
    names = [x["name"] for x in pc.list_indexes()]

 
  



