# Preservation and factual delta

Keep originals and the user's explicit decisions. Prefer a minimal diff when editing.
Preserve protected regions, quotes, numbers, units, denominators, negation, modality,
certainty, population, time range, causal language, citations, terminology and limits.
Use the task glossary; do not silently normalize literary or technical meanings.

After polish/translation compare those factual dimensions. Route new or strengthened
factual claims to evidence checking; unresolved deltas block fidelity acceptance even
when style improves. Pure style work on supplied facts does not require a new search.

Keep failed receipts and old revisions. Changed source/profile/input/artifact hashes
invalidate affected descendants, including rendered visual QA. Reconcile outstanding
attempt handles before retry after a timeout. Roll back only owned changes whose
current hashes still match the transaction; preserve later user edits as conflicts.

## Input preservation

Inputs and templates are read-only. Write outputs to a new path; an output path
equal to an input path fails unless the user explicitly asked for the overwrite
and the preimage was kept. Hash every input before and after the attempt. When an
edit in place is authorized, keep encoding, BOM, line endings and every line
outside the edited region byte-for-byte. Keep temporary backups and preimages
inside the workspace, never in `/tmp` or another location outside it.

Validator: [`check-receipt.py`](../../scripts/check-receipt.py) `verify --receipt <receipt> --workspace <dir>` checks input hashes and EOL before/after, the declared mutation and the preimage.
