import logging
from typing import Literal
from module_1.config import get_settings
from module_1.models import AgentState, RouteDecision, EvidenceGrade
from module_3.llm import get_llm
from module_2.vectorstore import get_retriever
from module_3.search import search_web

logger = logging.getLogger(__name__)
settings = get_settings()


def add_trace(state: AgentState, message: str) -> list[str]:
    return [*state.get("trace", []), message]
