from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from module_1.config import get_settings

settings = get_settings()

_llm = None
_groq_llm = None
