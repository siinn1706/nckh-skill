# Research, writing and visuals

Research modes keep search/screening protocols and reader cards; evidence keeps
identity/locator/support/counterevidence distinct. Method supports empirical and
literary argument/comparison without inventing results.

`nckh-humanwrite` owns prose polish and translation, including paper paragraphs.
`nckh-paperwrite` owns evidence-based outlines, sections, arguments, reporting
revisions and reviewer responses. `nckh-write` keeps the compatibility route and
general drafting. Both writers accept `--en` or `--vi`; conflicting flags stop
before editing. Without a flag, resolve the user's explicit target, brief, then
draft language; ask one question if unresolved. Bilingual requests remain usable.
Task glossary, protected regions and factual deltas apply to every route.
Taste is an advisory critic, not human gold. Read the shared
[language policy](../core/profiles/style/writer-language.md) and scoped
[writer resources](../core/profiles/style/writer-resources.md) for applicability.
[Venue profiles](../core/profiles/venue/isolation.md) isolate journal/conference,
year/track/article type and ranking system/category/year.

[Native document binding](../extensions/native-documents/contract.json) retains an
unavailable/null bundled default. A trusted task can separately select a permitted
SVG renderer with an explicit project/task/host
[binding record](../core/contracts/visual-engine-binding.schema.json). The record
stays in that project's task output, outside source/dist, and references actual
version/render process receipts and their input SVG/output PNG/log bytes. Bind the
absolute executable path, current SHA-256 and observed version; all observation
references are canonical project-relative paths. Its capability is only
`svg-render`, not native editing or scientific acceptance.

Run the portable [read-only checker](../scripts/check-visual-engine.py):

```text
python -I <relocated-checker-path> --project <absolute-project-root> --task <task-id> --host <claude|codex|cursor|agy> --binding <project-relative-binding.json> --capability svg-render
```

The checker uses its packaged [schema validator](../core/schema.py) and does not
invoke/install the engine or call a provider. Each closed process receipt includes
`command`, `exit_status=0`, `executable_sha256`, exact `version`, hashed project-relative
`stdout`/`stderr` references, `status=completed-unreviewed` and
`cleanup=owned-process-group-closed`. The version command must be the selected
executable with `--version`, with matching version output. The render receipt also
binds `input_sha256`/`render_sha256`; its command names that exact SVG and PNG using
`-o`/`--output`/`--output=`, optionally `--format png` or `--format=png`. Shell wrappers,
extra engine flags, missing evidence, drift and project/task/host mismatches fail
closed. Invalid explicit bindings do not fall back; absent bindings remain
unavailable. Integrity checks cannot authenticate a fabricated receipt or grant
permissions: the controller retains actual host observations and authorization.

An accepted task binding leaves global/default extension status unchanged and
allows the authorized host to create SVG source and call only the observed renderer
route. The final handoff still includes the SVG, final render and hash-bound QA:
source-to-mark mapping, real open/render/editability evidence and unresolved gates.
An earlier engine probe does not qualify the final artifact. Charts require real
data, mechanisms source/inferred edges and artwork an illustrative label.
Scientific meaning, native editability, render/accessibility and exact final hashes
have independent gates.

Research-domain skills are experimental. Corpus rights, human VI/EN/domain reviewers
and native visual receipts remain required for stable qualification.

Optional reporting, publisher and language reference snapshots use a standalone
reader and explicit [rights/provenance contract](contracts.md). Reporting lookup
serves matching clinical/health study designs; publisher profiles retain dated and
stale warnings; the English fragment supplies optional language advice.

Five separate actual-source packs supply bounded Wikisource passages, PMC article
excerpts, dated published World Bank observations, pinned Django code fixtures and
the first ten UCI Bank Marketing rows. The World Bank pack supplies observed chart
values with its snapshot date, source hashes and blank-unit caveat. The bounded
VI/PMC samples are not complete genre corpora or human gold. Exact venue policy,
factual fidelity, human taste, scientific acceptance and final visual QA retain
their separate gates.

## Scientific data and evaluation

| Task | Owning skill and contract |
|---|---|
| Scientific intake, provenance, quarantine and frozen partitions | [nckh-dataset](../skills/core/nckh-dataset/SKILL.md); dataset/split manifests |
| Estimand, independent units, dependence, uncertainty and readout | [nckh-statistics](../skills/core/nckh-statistics/SKILL.md); statistical analysis |
| Telemetry fields, units, time, correlation, joins and coverage | [nckh-telemetry](../skills/core/nckh-telemetry/SKILL.md); telemetry manifest |
| RCA, anomaly, forecasting, retrieval and agent evaluation | [nckh-aiops](../skills/core/nckh-aiops/SKILL.md); AIOps evaluation |

Database/migration remains with `nckh-data`; campaign KPIs and marketing A/B
remain with `nckh-analytics` and `nckh-experiment`. Telemetry normalization does
not infer a cause. Method owns design, cook owns authorized attempts and devops
owns environment/process observations. The
[reproducibility reference](../skills/core/nckh-method/references/reproducibility.md)
links the contained read-only graph checker. It never runs a manifest command.

Readouts bind exact dataset/split/run outputs and recompute declared metrics.
Ranking preserves the selected failed-unit denominator and undefined/zero-gold
policy; retrieval IDs and grades must belong to the frozen corpus and scale.
Retain failures, unknown costs, dependent units and retrospective availability
limits. Simulation requires a label and hash-bound parameters in every run.
No generic training engine, provider, collector, scheduler or remediation service
is installed by these skills.

## Research visual purpose

The [purpose guard](../core/guards.py) requires a research question/object, artifact
role, evidence origin, rights/access and source-to-mark mapping. It accepts actual
measurements, derived/computational/simulation outputs bound to real source,
code, transformation and completed run references, sourced mechanisms with
inferred edges labeled, or research illustrations labeled
`illustrative/non-evidentiary`. Computed outputs retain the label
`not observed measurements`. Blank source units stay blank.

Advertising, banners, logos (including research logos), thumbnails and generic
art do not pass the purpose gate through direct or indirect skill routes.
The guard performs read-only integrity checks before generation; it does not run
a simulation or authenticate source truth or fabricated receipts. See
[scientific visual QA](../skills/core/nckh-visuals/references/scientific-visual-qa.md)
for raw/transform/presentation bindings, table checks and final review.
Engine integrity, rights, native editing/rendering, accessibility and scientific
review remain independent gates. An unqualified host has a manual checker route;
packaged code alone does not establish preventive native enforcement.
