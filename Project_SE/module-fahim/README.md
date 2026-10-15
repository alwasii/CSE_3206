# module-fahim — Agentic QA Workflow (module-3)

Fahim 24524203101 | Ported from `Agentic-RAG-System/modules/module_3/`

## Files

- `llm.py` — OpenAI + Groq client factories and provider dispatcher
- `search.py` — Tavily web-search client with citation parsing
- `workflow_nodes.py` — LangGraph nodes: route → retrieve → grade → web fallback → rewrite → generate
