# Research visual QA

Locally authored, selectively informed by K-Dense, MIT, copyright 2025 K-Dense Inc.
The local archive has no verified whole-archive commit. Exact inspected sources:

- `resources/scientific-agent-skills-main/skills/scientific-visualization/SKILL.md`, SHA-256 `8cbde7cdc10d959cf72cfd08335cc8ce996247eee6ebdb900eb64a4cb0ff34a3`.
- `resources/scientific-agent-skills-main/skills/scientific-visualization/references/publication_guidelines.md`, SHA-256 `5f70c6b22dbb5e0fae18b0f1197b8794896bf7afc059874bcf7afbd5aa86bbe5`.
- `resources/scientific-agent-skills-main/skills/scientific-writing/references/figures_tables.md`, SHA-256 `212d10f3e7a01325d2518c4aab54a4fc04a67e4aa94e959cead199c425a0f4d6`.
- Root `LICENSE.md`, SHA-256 `09b02a3c9df3053c55531d503357a9c7cde275970e6c3ceaa1ddf5f0e90b40c1`.

This policy re-authors bounded QA decisions; it copies no upstream code, tables,
templates or package. Publisher-specific rules require the actual isolated venue
profile; general heuristics cannot certify a paper or scientific meaning.

| Check | Artifact evidence | Pending/failure condition |
|---|---|---|
| Purpose | Research question/object/role and evidence IDs | Research wording alone; branding or unrelated art |
| Data and mapping | Every value, label, arrow and table cell maps to source/run output or labeled inference | Missing mark, invented value, source mismatch |
| Origin and uncertainty | Observed vs derived/computed/simulation; model, run and caveat | Computation presented as observation; absent run or uncertainty |
| Reading | Units, denominators, legend, caption, alt text and readable typography | Blank source unit silently replaced; unexplained transform |
| Native and render | Actual final source/render/manifest hashes and opener evidence | Screenshot/file extension substituted for native editability |
| Rights and science | Dated provenance, applicable rights, reviewer/domain gate | Hashes or a structural pass treated as truth/approval |

Tables keep values/units/denominators and provenance; choose a figure only when it
helps the actual question. A schematic's arrow does not create causal evidence.
Any source, data, mark, source artifact, render or manifest change stales affected QA.
