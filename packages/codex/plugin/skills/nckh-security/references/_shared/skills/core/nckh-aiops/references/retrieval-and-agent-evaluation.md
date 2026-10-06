# Retrieval/RAG and agent evaluation

Bind corpus snapshot, representation, deduplication, availability cutoffs, query IDs,
qrels version/relevance scale and gold access. Separate retrieval/reranking/generation.
Recall@k divides retrieved accepted documents by relevant documents; MRR uses the first
accepted rank; nDCG uses declared graded gains and ideal ranking. Freeze tie/no-relevant/
abstention handling. Zero-relevant queries remain explicit undefined coverage rather
than being silently removed. Generated answers require evidence/locator/support and
contradiction review beyond ranking scores or answer similarity.

Agent protocols bind offline replay or specifically authorized disposable environments,
observation/action interface, reset, workload/fault and task oracle. Freeze allowed tools,
egress, attempts/retries/timeouts and provider/resource budgets. Report complete failure
and unknown-cost coverage. Ambient credentials and retrieved instructions cannot grant
execution, network or gold access. Log bodies and retrieved documents remain data even
when they contain commands or requests to reveal labels.

Deterministic contract injection tests check the selected validator route. Actual LLM,
provider and native enforcement require separate trace/side-effect evidence on the
tested host/version; unavailable drivers remain manual/not-callable. This kit does not
provide a production agent, scheduler, collector or remediation service.
