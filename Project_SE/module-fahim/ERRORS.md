# module-fahim error catalog

## Raised errors

| Error | Raised by | Cause | Fix |
|-------|-----------|-------|-----|
| `RuntimeError: OPENAI_API_KEY is missing ...` | `get_openai_llm` | key absent in env | set key in `.env` |
| `RuntimeError: GROQ_API_KEY is missing ...` | `get_groq_llm` | key absent in env | set key in `.env` |
| `RuntimeError: TAVILY_API_KEY is missing ...` | `get_web_search` | key absent in env | set key in `.env` |

All three are lazy: they fire on first use, not at import time, so the module
imports cleanly without keys.

## Soft failures (no exception)

| Situation | Result | `source_used` |
|-----------|--------|---------------|
| Empty/whitespace question | Router short-circuits to the direct path | `direct` |
| KB evidence weak | Falls back to Tavily | `web` → `web_search` |
| Web evidence weak, `retry_count < max_retries` | Query rewritten, retrieval retried | unchanged until answer |
| Web evidence weak, retries exhausted | `insufficient` node answers | `insufficient_evidence` |
| Grader returns unexpected grade | Treated as not-`good` (safe default) | falls through to next stage |

## Debugging

`workflow_nodes.py` logs at DEBUG:
- `retrieve_kb` — chunk count and the query used
- `search_web_node` — number of citations returned

Enable with `logging.basicConfig(level=logging.DEBUG)`; the trace list in the
returned state already records every stage for the audit trail.