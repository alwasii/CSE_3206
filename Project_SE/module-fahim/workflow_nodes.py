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
        "trace": add_trace(state, f"Router \u2192 {decision.route.upper()}"),
    }


def route_after_router(state: AgentState) -> Literal["retrieve_kb", "direct_answer"]:
    return "retrieve_kb" if state["source_used"] == "kb" else "direct_answer"


def retrieve_kb(state: AgentState) -> dict:
    docs = get_retriever().invoke(state["current_query"])
    return {
        "kb_docs": docs,
        "trace": add_trace(state, f"Private KB retrieval \u2192 {len(docs)} chunks"),
    }


def grade_kb(state: AgentState) -> dict:
    grader = get_llm("groq").with_structured_output(EvidenceGrade, method="json_mode")
    context = "\n\n".join(
        f"Source: {d.metadata.get('source', 'unknown')}\n{d.page_content}" for d in state["kb_docs"]
    )
    grade = grader.invoke(f"""
You grade evidence for an enterprise IT support assistant.
Question: {state['question']}
Private company KB evidence:
{context}
Return good only if the evidence is sufficient to answer confidently and specifically.
Otherwise return weak. JSON: {{\"grade\":\"good\"}} or {{\"grade\":\"weak\"}}.
""")
    return {
        "kb_grade": grade.grade,
        "trace": add_trace(state, f"KB evidence grade \u2192 {grade.grade.upper()}"),
    }


def after_kb(state: AgentState) -> Literal["generate_from_kb", "search_web"]:
    return "generate_from_kb" if state["kb_grade"] == "good" else "search_web"


def search_web_node(state: AgentState) -> dict:
    web_text, citations = search_web(state["current_query"])
    return {
        "web_results": web_text,
        "citations": citations,
        "source_used": "web",
        "trace": add_trace(state, "Web fallback \u2192 Tavily search"),
    }


def grade_web(state: AgentState) -> dict:
    grader = get_llm("groq").with_structured_output(EvidenceGrade, method="json_mode")
    grade = grader.invoke(f"""
Question: {state['question']}
Web evidence:
{state['web_results']}
Return good if the evidence is sufficient and directly relevant; otherwise weak.
Return valid JSON like {{\"grade\":\"good\"}}.
""")
    return {
        "web_grade": grade.grade,
        "trace": add_trace(state, f"Web evidence grade \u2192 {grade.grade.upper()}"),
    }


def after_web(state: AgentState) -> Literal["generate_from_web", "rewrite_query", "insufficient"]:
    if state["web_grade"] == "good":
        return "generate_from_web"
    if state["retry_count"] < settings.max_retries:
        return "rewrite_query"
    return "insufficient"


def rewrite_query(state: AgentState) -> dict:
    rewritten = get_llm("groq").invoke(f"""
Rewrite this IT support question for better private knowledge retrieval and vendor web search.
Preserve intent, add useful technical keywords, do not answer, return only the query.
Question: {state['question']}
""").content.strip()
    return {
        "current_query": rewritten,
        "retry_count": state["retry_count"] + 1,
        "trace": add_trace(state, f"Query rewrite \u2192 {rewritten}"),
    }


def generate_from_kb(state: AgentState) -> dict:
    context = "\n\n".join(
        f"[Source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}" for d in state["kb_docs"]
    )
    answer = get_llm("groq").invoke(f"""
You are an enterprise IT support copilot. Answer ONLY from the private company KB below.
Be concise, actionable, and safe. If steps are present, present them clearly.
Do not invent policy details. Mention that the answer is based on the company's private knowledge base.
Question: {state['question']}

Private KB:
{context}
""").content
    citations = []
    seen = set()
    for d in state["kb_docs"]:
        src = d.metadata.get("source", "Private KB")
        if src not in seen:
            seen.add(src)
            citations.append({"title": src.split("/")[-1], "url": "", "type": "private_kb"})
    return {
        "answer": answer,
        "source_used": "private_kb",
        "citations": citations,
        "trace": add_trace(state, "Answer generation \u2192 PRIVATE KB"),
    }
