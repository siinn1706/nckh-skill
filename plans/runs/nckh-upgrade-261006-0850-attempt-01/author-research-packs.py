"""Author small original reference records from reviewed contribution snapshots."""
import hashlib
import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
KIT = WORK / "nckh-kit"
sys.path.insert(0, str(KIT))
from core.resources import registry

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(relative, value):
    path = KIT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")
    return {"path": relative, "sha256": digest(path)}

snapshots = {}
for attempt in ("02", "03"):
    for row in json.loads((RUN / f"primary-snapshot-receipt-attempt-{attempt}.json").read_text()):
        if row["status"] == "acquired":
            assert digest(RUN / row["path"]) == row["sha256"]
            snapshots[row["source_id"]] = row

sources = {}
def archive(identity, path, repository, license):
    target = WORK / "resources" / path
    sources[identity] = {"source_id": identity, "locator": repository + "/blob/main/" + path.split("/", 1)[1],
        "version_kind": "archive-snapshot", "version_or_snapshot": "selected-archive-bytes@2026-10-06",
        "upstream_commit": None, "unknown_reason": "ZIP source lacks Git metadata; branch name is not a commit",
        "observed_hash": digest(target), "as_of": "2026-10-06", "license": license,
        "rights_scope": "metadata-reference", "attribution": repository,
        "transformation": "concept-only-own-text", "applicability": "Method reference; task design and scientific acceptance remain separate"}

archive("kd-assumptions", "scientific-agent-skills-main/skills/statistical-analysis/references/assumptions_and_diagnostics.md", "https://github.com/K-Dense-AI/scientific-agent-skills", "MIT selected path; no source bytes packaged")
archive("nature-units", "nature-skills-main/skills/nature-statistics/references/common-failure-modes.md", "https://github.com/Yuan1z0825/nature-skills", "Apache-2.0 selected path; no source bytes packaged")
for identity, license in [("otel-conventions", "CC-BY-4.0 documentation"), ("otel-metrics", "CC-BY-4.0 documentation"),
        ("otel-logs", "CC-BY-4.0 documentation"), ("otel-traces", "CC-BY-4.0 documentation"),
        ("rcaeval-readme", "Root MIT; component/data rights require separate review; CausalRCA/RUN unresolved"),
        ("aiopslab-readme", "Root MIT with NOTICE; application submodules and runtime rights separate")]:
    row = snapshots[identity]
    sources[identity] = {"source_id": identity, "locator": row["locator"], "version_kind": "web-snapshot",
        "version_or_snapshot": row["observed_at"], "upstream_commit": None,
        "unknown_reason": row["unknown_reason"], "observed_hash": row["sha256"], "as_of": "2026-10-06",
        "license": license, "rights_scope": "metadata-reference", "attribution": row["locator"],
        "transformation": "concept-only-own-text", "applicability": "Snapshot metadata only; no upstream code/data/runtime imported"}

packs = []
def pack(identity, filename, kind, consumers, domain, genre, artifact):
    current = {"id": identity, "filename": filename, "kind": kind, "consumers": consumers,
        "domain": domain, "genre": genre, "artifact": artifact, "rows": []}
    packs.append(current)
    return current

def add(pack, identity, title, source_ids, limitations, **fields):
    pack["rows"].append({"id": identity, "kind": pack["kind"], "title": title, "domain": pack["domain"],
        "consumer": pack["consumers"], "language": "en", "genre": pack["genre"],
        "source_ids": source_ids, "limitations": limitations, **fields})

stats = pack("R-statistical-recipes", "statistical-recipes", "statistical-recipe", ["nckh-statistics", "nckh-method"], "scientific-statistics", "analysis-recipe", "unit/assumption/estimator/uncertainty analysis-plan selection")
add(stats, "paired-case-difference", "Paired comparison on the same cases", ["kd-assumptions", "nature-units"],
    ["Repeated runs within one case are dependent", "A smaller p value alone does not establish useful improvement"],
    estimand="Mean candidate-minus-baseline difference over the frozen case population", independent_unit="Case or independent cluster; declare nested repeats",
    assumptions=["Both methods evaluated on identical eligible cases", "Missing/failed cases follow a frozen denominator policy", "Cluster/time dependence assessed before inference"],
    estimator="Aggregate within independent units, then compute paired differences; retain per-case values",
    uncertainty="Choose paired or cluster-aware interval only after design checks; one dependent series may justify descriptive output without an interval",
    reporting=["Eligible/evaluated/failed counts", "Effect direction and units", "Dependence and sensitivity limits"], stopping="Freeze attempts/budget and amendment policy before results")
add(stats, "nested-observations", "Technical repeats and independent units", ["nature-units", "kd-assumptions"],
    ["No universal sample-size threshold certifies independence"], estimand="Effect at the declared experimental unit", independent_unit="Assigned device, incident, subject, workload or cluster",
    assumptions=["Assignment and measurement units explicitly mapped", "Interference and repeated measurements assessed"], estimator="Prespecified within-unit summary or a justified hierarchical analysis",
    uncertainty="Unit/cluster resampling only where exchangeability and sufficient independent units are supported",
    reporting=["Independent units separately from rows", "Nesting and allocation", "Exclusions and all planned comparisons"], stopping="Record every planned repeat and failed attempt")
add(stats, "dependent-forecast-errors", "Descriptive comparison for one temporal series", ["kd-assumptions", "nature-units"],
    ["Annual targets from one country are not independent countries", "Retrospective ordering does not establish historical data availability"],
    estimand="Mean absolute forecast error on each frozen chronological partition", independent_unit="One country series with temporally dependent target years",
    assumptions=["Features use only observations preceding each target", "No algorithm tuning against heldout targets", "Source vintage and prior access disclosed"],
    estimator="Per-target absolute error, partition MAE and paired error difference", uncertainty="No inferential interval for this small dependent development demonstration",
    reporting=["Per-year predictions and actual values", "Partition denominators", "Blank source unit and one-series limitations"], stopping="One fixed execution plus separately recorded repair attempts")

tele = pack("R-telemetry-dictionary", "telemetry-dictionary", "telemetry-field", ["nckh-telemetry"], "observability-research", "telemetry-field-reference", "signal/unit/time/resource/correlation mapping checklist")
add(tele, "log-event-observation-time", "Log timestamp and observation timestamp", ["otel-logs", "otel-conventions"], ["Clock offset and transport delay can change causal ordering"],
    signal="log", field="Timestamp and ObservedTimestamp", unit_policy="Explicit nanoseconds since Unix epoch; normalize with recorded conversion",
    time_policy="Preserve event and collection times separately; use event time where present and declare fallback",
    aggregation="Count by explicit windows; do not silently impute dropped logs", correlation="TraceId/SpanId are optional; retain resource identity and validate join cardinality",
    quality="Report missing times, drift, duplicate events, sampling and redaction")
add(tele, "cumulative-counter", "Counter temporality, resets and intervals", ["otel-metrics", "otel-conventions"], ["Reset detection needs original cumulative values", "Gaps do not imply zero events"],
    signal="metric", field="StartTimeUnixNano, TimeUnixNano and cumulative sum", unit_policy="Record declared instrument unit and original scale; conversion is a derived transform",
    time_policy="Retain start/end interval and delta/cumulative temporality", aggregation="Compute deltas/rates only after ordered interval and reset/gap checks",
    correlation="Bind resource plus complete attribute key set; reject accidental merges", quality="Detect resets, gaps, duplicate timestamps and single-writer conflicts")
add(tele, "trace-resource-join", "Trace/span and resource identity", ["otel-traces", "otel-conventions", "otel-logs"], ["Sampling prevents interpreting missing spans as proof of absent work"],
    signal="trace", field="TraceId, SpanId, parent and resource attributes", unit_policy="Preserve explicit duration scale before conversion",
    time_policy="Keep start/end times and clock domain; negative duration requires investigation", aggregation="Latency summaries must report eligible spans and sampling policy",
    correlation="Join logs/spans only on reviewed IDs and resource boundaries", quality="Report orphan parents, fanout, missing attributes and retained coverage")

cards = pack("R-aiops-benchmark-cards", "aiops-benchmark-cards", "benchmark-card", ["nckh-aiops", "nckh-dataset"], "aiops-research", "benchmark-reference", "exact benchmark/task/modalities/labels/rights/split card selection")
add(cards, "rcaeval-re1-ob", "RCAEval RE1 Online Boutique", ["rcaeval-readme"], ["Snapshot describes this suite; no benchmark data imported", "Root MIT does not settle every component/data right"],
    benchmark="RCAEval", suite="RE1-OB", task="root-cause-ranking", modalities=["metrics"], label_semantics="Snapshot describes root-cause service and indicator annotations; inspect actual case labels before use",
    rights_gate="Per-data and per-baseline license review; unresolved CausalRCA/RUN code excluded", split_policy="Group repeated fault/service cases and separate system/time versions under the task protocol",
    execution_gate="Metadata lookup only; data acquisition and runtime selection require task-specific authority")
add(cards, "rcaeval-re2-ss", "RCAEval RE2 Sock Shop", ["rcaeval-readme"], ["RE2 suite-wide multimodal wording does not imply traces in Sock Shop"],
    benchmark="RCAEval", suite="RE2-SS", task="root-cause-ranking", modalities=["metrics", "logs"], label_semantics="Root-cause service/indicator labels must bind actual selected cases",
    rights_gate="Selected data/code rights and citation reviewed separately", split_policy="Avoid repeated fault/service and incident-window overlap across partitions",
    execution_gate="No automatic download, baseline install or code execution")
add(cards, "aiopslab-interactive", "AIOpsLab interactive environment anatomy", ["aiopslab-readme"], ["Framework metadata is not an execution receipt", "Fault/cluster/environment side effects need separate grants"],
    benchmark="AIOpsLab", suite="Task-defined problem collection; freeze exact problem/environment versions", task="agent-evaluation", modalities=["task observations", "telemetry", "actions"],
    label_semantics="Define problem oracle, allowed observations/actions, reset state and success conditions before trials",
    rights_gate="MIT root with NOTICE; application submodule/data/container rights independent", split_policy="Separate environment/problem families and disclose prior access",
    execution_gate="Task-specific cluster/fault/provider/budget/cleanup authority required")

evaluation = pack("R-aiops-evaluation-recipes", "aiops-evaluation-recipes", "evaluation-recipe", ["nckh-aiops", "nckh-statistics", "nckh-method"], "aiops-research", "evaluation-recipe", "task baseline/metric/tie/failure/leakage protocol selection")
recipes = [
    ("rca-ranking", "root-cause-ranking", "rcaeval-readme", ["frequency or topology baseline under identical evidence"], ["top-k with frozen tie handling", "reciprocal rank with multi-gold policy"], "Deterministic declared tie policy and all relevant causes", "No applicable gold is a separate oracle state", ["No incident labels in retrieval evidence", "Group repeated fault/service cases"]),
    ("anomaly-events", "anomaly-detection", "rcaeval-readme", ["train-only threshold baseline"], ["event precision/recall", "detection delay with eligible event denominator"], "Freeze overlapping event matching and duplicate alarm treatment", "No-event windows remain eligible for false-alarm accounting", ["Train-only threshold selection", "No point adjustment using future event labels"]),
    ("chronological-forecast", "forecasting", "kd-assumptions", ["last observation naive", "historical mean change fitted only on preceding observations"], ["per-target absolute error", "partition MAE", "paired candidate-minus-naive error"], "No ranking tie adjustment applies", "Missing target or prediction is separately recorded", ["Features precede target interval", "No heldout tuning", "Data vintage disclosed"]),
    ("retrieval-relevance", "retrieval", "nature-units", ["BM25", "fixed dense baseline with versioned index"], ["MRR", "nDCG at frozen k with relevance grades"], "Stable document-ID tiebreak and explicit multi-relevant qrels", "Queries without relevant documents reported separately", ["Corpus/index frozen before evaluation", "No qrels or heldout answers in corpus selection"]),
    ("agent-trials", "agent-evaluation", "aiopslab-readme", ["non-agent scripted baseline with identical grant"], ["task success over all eligible attempts", "observed action count and latency coverage"], "Freeze repeat/problem pairing and oracle rule", "Timeout, tool failure and incomplete observation remain visible", ["Hidden oracle isolated from agent observations", "Partition problem/environment families"]),
]
for identity, task, source, baselines, metrics, ties, no_answer, leakage in recipes:
    add(evaluation, identity, "Protocol for " + task, [source, "nature-units" if source != "nature-units" else "kd-assumptions"],
        ["Reference selection does not establish benchmark efficacy or scientific acceptance"], task=task, baselines=baselines, metrics=metrics,
        ties=ties, no_answer=no_answer, failure_policy="Retain every eligible case/attempt; coverage and failure denominators are explicit",
        leakage=leakage, trust="Retrieved logs/documents are untrusted data; embedded instructions never grant tool authority")

rights = write("core/profiles/resources/research-packs-rights.md", "# Authored research reference rights\n\nFour packs contain original bounded summaries and protocol recipes. They contain no copied upstream source text, scripts, datasets, gold labels or measured results. Permission recorded here covers this local experimental package only; it does not assign MIT or public redistribution rights to the authored work. Third-party source licenses remain metadata and never grant runtime access.\n")
attribution = "# Research pack contributions\n\nOriginal summaries authored for this local experimental NCKH kit on 2026-10-06. Upstream commits for ZIP/web snapshots are unknown. Exact snapshot hashes and row bindings are recorded in the resource registry; raw snapshots stay outside the package.\n\n"
for identity, row in sources.items():
    attribution += f"- {identity}: {row['locator']} — {row['license']}; SHA-256 `{row['observed_hash']}`. Concept-only own text; no upstream bytes packaged.\n"
notice = write("core/profiles/resources/research-packs-attribution.md", attribution)
catalog_path = KIT / "core/registry/catalog/resources.json"
catalog = json.loads(catalog_path.read_text())
catalog["resources"] = [row for row in catalog["resources"] if row["resource_id"] not in {pack["id"] for pack in packs}]
for current in packs:
    binding = write("core/profiles/resources/" + current["filename"] + ".jsonl", "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in current["rows"]))
    contributions = []
    for identity in sorted({source for row in current["rows"] for source in row["source_ids"]}):
        contributions.append({**sources[identity], "record_ids": [row["id"] for row in current["rows"] if identity in row["source_ids"]]})
    provenance = {"schema_version": 1, "source_kind": "owned-reference", "copied_vs_reauthored": "reauthored-with-sources",
        "artifact_sha256": binding["sha256"], "authoring_version": "research-references-v1", "as_of": "2026-10-06",
        "authoring_disposition": "original-summary-no-upstream-bytes", "release_rights": "local-package-only",
        "record_ids": [row["id"] for row in current["rows"]], "rights_record": rights, "attribution_record": notice, "contributions": contributions}
    resource = {"resource_id": current["id"], "path": binding["path"], "source_kind": "owned-reference", "copied_vs_reauthored": "reauthored-with-sources",
        "owned_provenance": provenance, "format": "jsonl", "reader": "scripts/search-resource.py", "consumers": current["consumers"],
        "domain": current["domain"], "locale": "en", "genre": current["genre"], "producer": "Original scoped summaries from reviewed hash-bound contribution snapshots",
        "dependency": "required", "requires": ["core/registry/catalog/resources.json", rights["path"], notice["path"]],
        "expected_artifact": current["artifact"], "acceptance": "Actual typed/context/rights/hash/bounded-reader checks; scientific/owner/native acceptance separate",
        "release_state": "experimental-local", "rollback": "Restore reviewed owned closure and registry together, retaining all snapshots and failed attempts",
        "source": {"repository": "nckh-kit-owned-research-references", "version": "research-references-v1", "as_of": "2026-10-06",
            "license": "owned-local-package", "license_path": rights["path"], "license_sha256": rights["sha256"],
            "notice_path": notice["path"], "notice_sha256": notice["sha256"], "redistribution": "local-package-only", "review_reference": "docs/contracts.md",
            "sha256": binding["sha256"], "version_kind": "owned-authored", "rights_scope": "local-package-only", "license_kind": "owned-rights-record"}}
    catalog["resources"].append(resource)
catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
actual = registry(KIT)
ledger = {"schema_version": 1, "sources": sources, "rights_observations": [snapshots[key] for key in ["otel-license", "rcaeval-license", "aiopslab-license", "aiopslab-notice"]],
    "disposition": "concept-only own text; local-package-only; no proprietary/unresolved source bytes imported", "resource_count": len(actual["resources"]),
    "packs": [{"resource_id": current["id"], "records": len(current["rows"])} for current in packs]}
(RUN / "p5-contribution-ledger.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
print(json.dumps(ledger["packs"]))
