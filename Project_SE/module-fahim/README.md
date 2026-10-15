# module-fahim — Agentic QA Workflow (module-3)

Fahim 24524203101 | Ported from `Agentic-RAG-System/modules/module_3/`

## Files

- `llm.py` — OpenAI + Groq client factories and provider dispatcher
- `search.py` — Tavily web-search client with citation parsing
- `workflow_nodes.py` — LangGraph nodes: route → retrieve → grade → web fallback → rewrite → generate

## Setup

1. Copy `.env.example` to `.env` and fill `OPENAI_API_KEY`, `GROQ_API_KEY`, `TAVILY_API_KEY`.
2. Keep the sibling-package import style (`module_1`, `module_2`, ...) — see `NOTES.md`.

## Flow

route_question → retrieve_kb → grade_kb → generate_from_kb (good) or
search_web_node → grade_web → generate_from_web (good) or
rewrite_query → retry (max_retries) or insufficient.
