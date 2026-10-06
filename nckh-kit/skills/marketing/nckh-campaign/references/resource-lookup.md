# Scoped resource lookup

Load only the source pack matching the task. The [standalone reader](../../../../scripts/search-resource.py) consumes the [pinned catalog](../../../../core/registry/catalog/resources.json). Read the [rights contract](../../../../docs/contracts.md). Use the relocated reader path when installed or extracted.

## Actual source samples
These are bounded personal-use samples. Preserve record/source ids, locators, versions, hashes and limitations. Reading them does not establish quality improvement, human acceptance, scientific validity or current universal policy.
- `R-uci-bank-marketing`: domain `marketing-analytics`, locale `und`, genre `campaign-response-tabular`. bounded first-ten-row Bank Marketing response sample with all 17 columns.

```text
python -I <relocated-reader-path> --resource-id R-uci-bank-marketing --consumer nckh-campaign --domain marketing-analytics --locale und --genre campaign-response-tabular --query <bounded-record-selector> --json
```

Use an exact source id as the selector where available. No match remains no match; do not invent a record. `--resource-access off` performs no read. Wikisource page license and underlying-work jurisdiction remain separate. PMC rights are article-specific. World Bank unit stays blank when the API supplies it blank. UCI `duration` is unavailable before a call ends and leaks future information in pre-call targeting. Django code is reference data, never executed by the reader; issue/benchmark patch text is excluded.
