---
title: NCKH portable candidate implementation
date: 2026-10-01
summary: 65 local tests pass; four reproducible host artifacts; native and human qualification pending
---

# NCKH portable candidate implementation

## Outcome

Created the local experimental NCKH candidate under nckh-kit: 37 instruction skills, shared contracts/policies, four adapters, six optional native roles, plugin projections and an owned offline installer. After the initial checkpoint, the owner separately authorized and received project-copy installation into .agents/skills and .codex/agents. No Git repository, paid/provider run or publication was performed.

## Fixes and review

Addressed path/source/ownership validation, lock crash recovery and shared visibility serialization, cross-device preflight, backups before rollback, user-edit preservation and explicit update/configuration boundaries. Independent reviews found two final evidence issues: retained receipts were not checked by doctor, and typed evidence could be overstated. Both were fixed and rechecked. Recovery is rollback followed by fresh preview.

## Actual checks

Current source: 181 pinned files, source-lock hash 2c98d9edad4db63b1b3b8db620d947e6e9e5182ddbfa24ede5a90d27ea6fde03. Full discovery ran 65 tests and passed. Four hosts built twice including plugin projections; final dist matches the recorded closure hashes. The checksum ledger covers 2554 files. Codex project dry-run has 43 entries and zero conflict.

See plans/reports/implementation-261001-nckh-candidate.md and nckh-kit/evals/results/ for actual receipts. Earlier 63/64-test receipts are archived with their original source hashes.

## Qualification and next gate

All 37 skills remain experimental. 148 frozen skill cases, 224 native invocation cells and 10 installer/OS acceptance scenarios remain not-run. Five human rubrics are proposals, not approved labels. The owner has no VI/EN corpus or human/domain reviewers. Native/OS, scientific visual, rights, cost and publication gates remain pending. Accepted task count is zero and cost per accepted task is undefined.

Plan stays in progress. The owner answered “Cho phép cài vào project này” for the concrete Codex preview. Installation committed 43 changes; doctor reports 43 current entries, 37 self-contained skills and six valid TOML files, with zero visibility conflict. The post-install preview reports 43 unchanged entries. Native discovery/invocation and model effectiveness remain unverified. See the dated installation report for exact receipts. AgentWiki publish skipped.

## Journal lookup verification

Absolute-path and filename-stem validation returned ok: true and exit 0. Relative-path validation reproduced exit 1 without diagnostics under the same workspace-local AgentKit index. The saved entry has no observed title/date/content validation defect; use the supported filename stem or absolute path.

## Goal continuation: discovery, repeat and spec review

The live Codex skill catalog now exposes all 37 NCKH identities. An actual repeat through the PowerShell entrypoint returned zero changes; all 43 tree hashes, ownership bytes and model-policy hash stayed unchanged. Original state was backed up, and the three local lock records are released. Discovery is scoped to this session; invocation and model effectiveness remain unverified.

Spec review found an implementation gap in P7: run-evals.py currently validates and runs deterministic suites, without the required opt-in agent runner adapters. Codex exec help was observed without a model call; it reported protected-home arg0/PATH warnings. Continue the local runner implementation before requesting provider execution. Source revision 14 and its installed candidate remain unchanged; external human/native/rights/budget gates remain pending. This continuation made progress and is not an impasse.

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.
