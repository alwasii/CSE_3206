# module-fahim — design notes (Fahim 24524203101)

## Why Groq for router + graders
Routing and evidence grading need cheap, fast structured JSON output.
Groq serves the small OSS model with json_mode, so every decision node
uses `get_llm("groq")` while generation can use either provider.

## Fallback chain
retrieve_kb → grade_kb → (good: generate_from_kb | weak: search_web) →
grade_web → (good: generate_from_web | weak: rewrite_query → retry |
retries out: insufficient). `max_retries` comes from module_1 settings.

## Citations
KB answers cite private sources (deduplicated by path); web answers cite
Tavily results with title + URL. Direct answers carry no citations.
