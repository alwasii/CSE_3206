# Worked example (Fahim 24524203101)

Two sample questions traced through the module-3 nodes.

## Example 1 — KB answers it

**Q:** "How do I reset my VPN password?"

| Step | Node | Result |
|------|------|--------|
| 1 | `route_question` | `source_used="kb"` (VPN is an IT topic) |
| 2 | `retrieve_kb` | 4 chunks from `data/sample_kb/vpn_setup.md` |
| 3 | `grade_kb` | `good` — steps are present and specific |
| 4 | `generate_from_kb` | grounded answer + citation `vpn_setup.md` |

Answer text reminds the user it is based on the company's private KB.

## Example 2 — web fallback + rewrite

**Q:** "Does the new Acme Dock 900 support LDAP passthrough?"

| Step | Node | Result |
|------|------|--------|
| 1 | `route_question` | `source_used="kb"` (device question) |
| 2 | `retrieve_kb` | 2 chunks, none mention Dock 900 |
| 3 | `grade_kb` | `weak` — evidence does not answer confidently |
| 4 | `search_web_node` | Tavily returns vendor docs, 5 citations |
| 5 | `grade_web` | `good` — vendor page covers LDAP |
| 6 | `generate_from_web` | answer flagged as external, needs IT validation |

If step 5 had returned `weak` and `retry_count == max_retries`, the graph
routes to `insufficient` instead of looping forever.

## Trace output

Every node appends a human-readable line to `state["trace"]`, for example:

```
Router → KB
Private KB retrieval → 4 chunks
KB evidence grade → GOOD
Answer generation → PRIVATE KB
```

This trace is what `module-Nayem/api_routes.py` returns in `ChatResponse.trace`
and what `module-shanto/audit.py` stores.