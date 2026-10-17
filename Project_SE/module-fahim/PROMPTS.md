# module-fahim prompt catalog

Every prompt is an inline f-string in `workflow_nodes.py`. Kept here so the
wording is reviewable without reading code.

## 1. Router (`route_question`, Groq + json_mode)
Decides `kb` vs `direct`. Lists KB topic hints (IT policies, VPN, password
reset, MFA, laptop setup, software access, security, email, devices,
troubleshooting). `direct` is only for greetings/thanks/casual chat.
Output: `{"route":"kb"}`.

## 2. KB grader (`grade_kb`, Groq + json_mode)
Returns `good` only when private-KB evidence is sufficient to answer
confidently and specifically, else `weak`. Output: `{"grade":"good"}`.

## 3. Web grader (`grade_web`, Groq + json_mode)
Same `good`/`weak` shape, judged on web evidence for sufficiency and direct
relevance.

## 4. Query rewriter (`rewrite_query`, Groq)
Rewrites for better private-KB retrieval and vendor web search. Rules:
preserve intent, add technical keywords, do not answer, return only the query.

## 5. KB generator (`generate_from_kb`, Groq)
System role: enterprise IT support copilot, answer **only** from the private
KB. Concise, actionable, safe; present steps clearly; never invent policy
details; state that the answer comes from the private knowledge base.

## 6. Web generator (`generate_from_web`, Groq)
Runs only when the private KB was insufficient. Answer **only** from web
evidence and explicitly flag that it is external web information needing IT
validation before changing company-managed systems.

## 7. Direct responder (`direct_answer`, Groq)
Brief, natural reply for non-KB chat; no retrieval, no citations.

## Grounding rule
Both generators are given evidence and nothing else, so unsupported claims
have no source to come from — this is the anti-hallucination mechanism.