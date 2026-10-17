# module-fahim API reference

## `llm.py`

| Function | Returns | Notes |
|----------|---------|-------|
| `get_openai_llm() -> ChatOpenAI` | OpenAI chat model | Lazy singleton; raises if `OPENAI_API_KEY` empty |
| `get_groq_llm() -> ChatGroq` | Groq chat model | Lazy singleton; raises if `GROQ_API_KEY` empty |
| `get_llm(provider="openai")` | chat model | `"groq"` → Groq, anything else → OpenAI |

## `search.py`

| Function | Returns | Notes |
|----------|---------|-------|
| `get_web_search()` | Tavily tool | Lazy singleton; `max_results=5`, `topic="general"`, `include_answer=True` |
| `search_web(query)` | `(str, list[dict])` | `(evidence_text, citations)`; citations carry `title`, `url`, `type="web"` |

## `workflow_nodes.py`

All nodes take `AgentState` and return a partial-state `dict`. `add_trace`
appends to `state["trace"]`.

| Node | Writes |
|------|--------|
| `route_question` | `source_used` (`kb`/`direct`), `trace` |
| `retrieve_kb` | `kb_docs`, `trace` |
| `grade_kb` | `kb_grade` (`good`/`weak`), `trace` |
| `search_web_node` | `web_results`, `citations`, `source_used="web"`, `trace` |
| `grade_web` | `web_grade`, `trace` |
| `rewrite_query` | `current_query`, `retry_count+1`, `trace` |
| `generate_from_kb` | `answer`, `source_used="private_kb"`, `citations`, `trace` |
| `generate_from_web` | `answer`, `source_used="web_search"`, `trace` |
| `direct_answer` | `answer`, `source_used="direct"`, `trace` |
| `insufficient` | `answer`, `source_used="insufficient_evidence"`, `trace` |

Conditional edges: `route_after_router`, `after_kb`, `after_web`.

`source_used` is the audit field module-shanto writes via `write_audit`.