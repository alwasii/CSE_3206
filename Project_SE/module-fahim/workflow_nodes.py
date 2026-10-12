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


def route_question(state: AgentState) -> dict:
    router = get_llm("groq").with_structured_output(RouteDecision, method="json_mode")
    decision = router.invoke(f"""
You route messages for an enterprise IT support assistant.
Use kb for questions about company IT policies, VPN, password reset, MFA, laptop setup,
software access, security, email, devices, troubleshooting, or technology support.
Use direct only for greetings, thanks, or casual chat that needs no company knowledge.
Question: {state['question']}
Return valid JSON like {{"route":"kb"}}.
""")
    return {
        "source_used": decision.route,
        "trace": add_trace(state, f"Router → {decision.route.upper()}"),
    }


def route_after_router(state: AgentState) -> Literal["retrieve_kb", "direct_answer"]:
    return "retrieve_kb" if state["source_used"] == "kb" else "direct_answer"


def retrieve_kb(state: AgentState) -> dict:
    docs = get_retriever().invoke(state["current_query"])
    return {
        "kb_docs": docs,
        "trace": add_trace(state, f"Private KB retrieval → {len(docs)} chunks"),
    }
