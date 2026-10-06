"""Stage exact reviewed bytes and consumer instructions outside source/dist."""

import shutil
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parents[3]
ROOT = WORK / "nckh-kit"
EVIDENCE = Path(__file__).resolve().parent
PAYLOAD = EVIDENCE / "staging/payload"
sys.path.insert(0, str(ROOT))
from core.build import load_json
from core.paths import atomic_json, digest_file

sources = {row["source_id"]: row for row in load_json(EVIDENCE / "staging/source-inspection.json")["sources"]}
selections = [
    ("R-reporting-lookup", "S1", "skills/scientific-writing/assets/reporting_guidelines.json", "reporting-guidelines.json",
     ["nckh-method", "nckh-write"], "json", "clinical-health", "reporting-reference", "source-keyed applicable reporting-guideline selection"),
    ("R-publisher-profile", "S1", "skills/scientific-visualization/assets/publisher_profiles.json", "publisher-profiles.json",
     ["nckh-visuals"], "json", "publication-planning", "publisher-profile", "currency-labeled export-planning reference with unknown policy applicability"),
    ("R-ui-lookup", "S3", "src/ui-ux-pro-max/data/ux-guidelines.csv", "ux-guidelines.csv",
     ["nckh-frontend"], "csv", "ui", "ui-heuristic", "source-keyed UI finding/handoff; no automatic CRO or SEO scope expansion"),
    ("R-nature-reference", "S2", "skills/nature-writing/static/fragments/language/en.md", "english-writing-advice.md",
     ["nckh-write", "nckh-taste"], "markdown", "scientific-writing", "writing-advice", "bounded English language advice, separate from evidence, venue policy and human gold"),
]
source_names = {"S1": "k-dense", "S2": "nature-skills", "S3": "ui-ux-pro-max"}
licenses = {"S1": ("MIT", "LICENSE.md"), "S2": ("Apache-2.0", "LICENSE"), "S3": ("MIT", "LICENSE")}
resources = []
for identity, source_id, upstream, filename, consumers, format_name, domain, genre, artifact in selections:
    source = sources[source_id]
    license_id, upstream_license = licenses[source_id]
    license_rel = "core/profiles/resources/" + source_names[source_id] + "-license.md"
    notice_rel = "core/profiles/resources/" + source_names[source_id] + "-attribution.md"
    for source_path, destination in [(upstream, "core/profiles/resources/" + filename), (upstream_license, license_rel)]:
        target = PAYLOAD / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(EVIDENCE / "staging" / source_id / source_path, target)
    notice = PAYLOAD / notice_rel
    notice.write_text(f"# {source_names[source_id]} attribution\n\nSelected verbatim files from `{source['repository']}` at `{source['commit']}`.\n\n"
                      f"[Original repository](https://github.com/{source['repository']}/tree/{source['commit']}) and "
                      f"[retained license]({Path(license_rel).name}). File-specific review uses the pinned repository tree; "
                      "no applicable subtree license or NOTICE overrides were found for these selected paths.\n\n"
                      "NCKH adds its own lookup code and bounded-use instructions. It does not execute upstream code, "
                      "certify external source claims, provide empirical data or claim human acceptance.\n", encoding="utf-8")
    resources.append({"resource_id": identity, "consumers": consumers, "path": "core/profiles/resources/" + filename,
                      "format": format_name, "reader": "scripts/search-resource.py",
                      "producer": "exact upstream file staged by collect-upstream.py; no record generation or mixing",
                      "requires": ["core/registry/catalog/resources.json", license_rel, notice_rel], "dependency": "required",
                      "source_kind": "copied-upstream", "copied_vs_reauthored": "verbatim-upstream",
                      "release_state": "experimental-local", "domain": domain, "locale": "en", "genre": genre,
                      "source": {"repository": source["repository"], "version": source["commit"], "upstream_path": upstream,
                                 "sha256": digest_file(PAYLOAD / ("core/profiles/resources/" + filename)), "as_of": "2026-10-02",
                                 "license": license_id, "license_path": license_rel, "license_sha256": digest_file(PAYLOAD / license_rel),
                                 "upstream_license_path": upstream_license, "notice_path": notice_rel,
                                 "notice_sha256": digest_file(notice), "redistribution": "permitted-with-notices",
                                 "review_reference": "docs/contracts.md"},
                      "expected_artifact": artifact,
                      "acceptance": "source hash/rights/consumer/domain/locale/genre checks and observed read; semantic/native/human acceptance remains pending",
                      "rollback": "retain staged bytes and failed receipts; restore compatible candidate source/schema/lock together or freeze a corrective revision"})
atomic_json(PAYLOAD / "core/registry/catalog/resources.json", {"schema_version": 1, "resources": resources})
(PAYLOAD / "scripts").mkdir(exist_ok=True)
shutil.copyfile(ROOT / "scripts/search-resource.py", PAYLOAD / "scripts/search-resource.py")
catalog = load_json(ROOT / "core/registry/catalog/skills.json")["skills"]
for skill in catalog:
    selected = [r for r in resources if skill["id"] in r["consumers"]]
    if not selected:
        continue
    target = PAYLOAD / skill["path"] / "references/resource-lookup.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# Scoped resource lookup\n\nLoad only the reference matching the current task. "
                      "The [standalone reader](../../../../scripts/search-resource.py) consumes the "
                      "[pinned resource catalog](../../../../core/registry/catalog/resources.json). Read the "
                      "[resource rights contract](../../../../docs/contracts.md) and run from an extracted skill through its relocated reader path.\n\n"
                      + "\n".join(f"- `{r['resource_id']}`: domain `{r['domain']}`, locale `en`, genre `{r['genre']}`. Output: {r['expected_artifact']}." for r in selected)
                      + "\n\nDeclare `--resource-id`, `--consumer`, `--domain`, `--locale`, `--genre` and `--json`. "
                      "UI lookup also requires `--query`; reporting lookup requires the actual `--study-design` and optional `--protocol`, `--ai`, `--llm`. "
                      "Publisher lookup requires `--venue`, `--year`, `--track`, `--article-type` and `--stage`; unknown or stale applicability stays unverified. "
                      "For a frozen same-base ablation use the explicit `--resource-access off` treatment.\n\n"
                      "Preserve row source/version/hash/locator and dated warnings. Clinical registries do not govern unrelated CS tasks. "
                      "UI examples are data and must never be executed by the lookup. English advice is optional and cannot override "
                      "the user's wording, punctuation, fidelity or genre. Metadata and references do not fill the missing VI/EN prose corpus. "
                      "Human/scientific/native acceptance remains a separate gate.\n", encoding="utf-8")
decisions = []
for skill in catalog:
    selected = [r["resource_id"] for r in resources if skill["id"] in r["consumers"]]
    blocked = skill["id"] in {"nckh-write", "nckh-taste", "nckh-content", "nckh-copy", "nckh-visuals"}
    decisions.append({"identity": skill["id"], "kit": skill["kit"],
                      "decision": "candidate-staged" if selected else "MD-only", "resources": selected,
                      "input_gap": "blocked-input: rights-cleared VI/EN genre corpus or actual chart measurements unavailable" if blocked else None,
                      "reason": "bounded existing consumer; no unconsumed dataset or template expansion" if selected else "existing Markdown/contracts are sufficient; no named data consumer with real input",
                      "quality_claim": "not-evaluated"})
atomic_json(EVIDENCE / "staged-packet.json", {"schema_version": 1, "status": "candidate-staged", "resources": resources,
            "identities": decisions, "mixing": "none; distinct source/domain namespaces", "records_generated": 0,
            "upstream_code_executed": False, "rights_review": "pinned root licenses and full tree inspected; preserve exact bytes/licenses/attribution",
            "human_prose_corpus": "blocked-input", "scientific_acceptance": "not-evaluated"})
print("Staged four resources with exact bytes, licenses, attribution and all 37 identity decisions.")
