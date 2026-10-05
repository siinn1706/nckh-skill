# Scoped resource lookup

Load only the source pack matching the task. The [standalone reader](_shared/scripts/search-resource.py) consumes the [pinned catalog](_shared/core/registry/catalog/resources.json). Read the [rights contract](_shared/docs/contracts.md). Use the relocated reader path when installed or extracted.

## Actual source samples
These are bounded personal-use samples. Preserve record/source ids, locators, versions, hashes and limitations. Reading them does not establish quality improvement, human acceptance, scientific validity or current universal policy.
- `R-django-sqlmigrate-fixtures`: domain `engineering-task`, locale `en`, genre `code-review-fixture`. bounded JSONL with two BSD-licensed Django fixture contents and task locators only.

```text
python -I <relocated-reader-path> --resource-id R-django-sqlmigrate-fixtures --consumer nckh-fix --domain engineering-task --locale en --genre code-review-fixture --query <bounded-record-selector> --json
```

Use an exact source id as the selector where available. No match remains no match; do not invent a record. `--resource-access off` performs no read. Wikisource page license and underlying-work jurisdiction remain separate. PMC rights are article-specific. World Bank unit stays blank when the API supplies it blank. UCI `duration` is unavailable before a call ends and leaks future information in pre-call targeting. Django code is reference data, never executed by the reader; issue/benchmark patch text is excluded.
