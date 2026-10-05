# Optional bounded writer lookups

Use the packaged [reader](../../../scripts/search-resource.py) with its resource
ID and the current writer as `--consumer`. Preserve source locale independently of
output language. Add `--resource-access off` when resources are disabled.

| Resource | Allowed writers | Required source filters |
|---|---|---|
| `R-nature-reference` | humanwrite, paperwrite | `--locale en --domain scientific-writing --genre writing-advice` |
| `R-vi-wikisource-passages` | humanwrite | `--locale vi --domain language-literary --genre prose-verse-samples` |
| `R-pmc-scientific` | humanwrite, paperwrite | `--locale en --domain scientific-writing --genre scientific-research-article` |
| `R-reporting-lookup` | paperwrite | `--locale en --domain clinical-health --genre reporting-reference --study-design <actual-design>` |

Writer IDs in commands include the `nckh-` prefix. Existing consumers retain their
rights; paperwrite does not inherit Wikisource or publisher access from `nckh-write`.
Check applicability and each returned source/license/lineage record. A missing,
wrong-consumer, wrong-locale/domain/genre, drifted or disabled pack is not read.
These snapshots are references, not complete corpora, human gold, new evidence,
universal venue policy or a certification of style/scientific quality.
