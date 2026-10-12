from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from module_1.config import get_settings

settings = get_settings()

_llm = None
_groq_llm = None


def get_openai_llm():
    global _llm
    if _llm is None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing")
        _llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0,
            api_key=settings.openai_api_key,
        )
    return _llm


def get_groq_llm():
    global _groq_llm
    if _groq_llm is None:
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is missing")
        _groq_llm = ChatGroq(
            model=settings.groq_model,
            temperature=0,
            api_key=settings.groq_api_key,
        )
    return _groq_llm


def get_llm(provider: str = "openai"):
    if provider == "groq":
        return get_groq_llm()
    return get_openai_llm()
