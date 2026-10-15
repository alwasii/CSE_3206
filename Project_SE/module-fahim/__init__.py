"""Fahim 24524203101 | module-3: agentic QA workflow (LLM + web fallback).

Source: Agentic-RAG-System/modules/module_3/
Files: llm.py, search.py, workflow_nodes.py

Note: sibling modules import each other as top-level packages
(module_1, module_2, ...), so this package keeps the same style
and exposes no eager imports here.
"""

__all__ = ["get_llm", "get_openai_llm", "get_groq_llm", "get_web_search", "search_web"]
