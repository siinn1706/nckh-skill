---
phase: 2
title: "Repair conversion and verify"
status: pending
---

# Phase 2: Repair conversion and verify

## Requirements

- All three tests pass; `owner-note.txt` stays unchanged.

## Files to modify

- `app.py` only.

## Steps

1. Change the conversion function.
2. Run the test module as its own command and record its exit status.

## Verification

- Back to [phase 1](./phase-01-reproduce-failure.md) for the failing baseline.

## Risk & rollback

Restore `app.py` from its recorded preimage if a test regresses.
