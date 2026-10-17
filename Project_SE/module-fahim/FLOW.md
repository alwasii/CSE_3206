# module-fahim workflow (graph)

```mermaid
flowchart TD
    start([question]) --> router{route_question}
    router -->|kb| retrieve[retrieve_kb]
    router -->|direct| direct[direct_answer]
    router -->|empty| direct

    retrieve --> gradekb{grade_kb}
    gradekb -->|good| genkb[generate_from_kb]
    gradekb -->|weak| web[search_web_node]

    web --> gradeweb{grade_web}
    gradeweb -->|good| genweb[generate_from_web]
    gradeweb -->|weak| rewrite[rewrite_query]
    rewrite --> retrieve
    gradeweb -->|retries out| insufficient[insufficient]

    genkb --> answer([answer + citations])
    genweb --> answer
    direct --> answer
    insufficient --> answer
```

## Nodes

| Node | Purpose |
|------|---------|
| `route_question` | LLM JSON decision: `kb` or `direct` |
| `retrieve_kb` | top-k private KB chunks |
| `grade_kb` | evidence strong enough to answer? |
| `search_web_node` | Tavily fallback when KB is weak |
| `grade_web` | web evidence strong enough? |
| `rewrite_query` | new retrieval round, bumps `retry_count` |
| `generate_from_kb` / `generate_from_web` | grounded answers |
| `direct_answer` / `insufficient` | no-retrieval paths |

`retry_count` vs `settings.max_retries` guards the rewrite loop.