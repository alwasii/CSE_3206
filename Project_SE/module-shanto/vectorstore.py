import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from module_1.config import get_settings
from module_1.embeddings import get_embeddings, get_embedding_dimension

settings = get_settings()

_vectorstore = None