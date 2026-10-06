# Counsel: inventory integration encoding failure

## TL;DR

`inventory-integration.py` uses `Path.read_text()` without an encoding on six
paths. On Windows this selects the process locale (`cp1252` here), while the
evaluation JSON contains UTF-8 multilingual bytes; the failure at line 26 is
therefore a run-script decoding defect. Add `encoding="utf-8-sig"` to every
text read in this script before retrying. No production or test change is
needed.

## Verified cause

- `plans/runs/nckh-upgrade-261006-0850-attempt-01/inventory-integration.py:20`
  reads `baseline.json` without an encoding.
- Line 21 reads the catalog without an encoding.
- Line 26 reads every evaluation-case JSON with `path.read_text()` and is the
  reported failure site. The default Windows decoder raises
  `UnicodeDecodeError` on byte `0x81` in a UTF-8 multilingual file.
- Line 42 reads each inventory surface without an encoding; line 50 reads
  `protected-hashes.json` without one; line 62 reads documentation files
  without one. A retry that fixes only line 26 would leave the same latent
  failure at a later input.
- `digest(path)` already uses `read_bytes()`, so hash computation is
  encoding-independent. `save()` already writes with `encoding="utf-8"`.
- The failure occurs before the first `save(...)` call near the end of the
  script, so the reported run produced no inventory/protected/link-check
  outputs before stopping.

## Minimal repair

In the run-local `inventory-integration.py`, make every `Path.read_text()`
explicitly UTF-8 capable:

```python
read_text(encoding="utf-8-sig")
```

Apply this consistently to the six reads at lines 20, 21, 26, 42, 50, and 62.
`utf-8-sig` accepts ordinary UTF-8 and strips an optional BOM, which is safe
for JSON, source text, and Markdown. Keep `digest(path.read_bytes())` and the
existing UTF-8 writer unchanged.

Do not rely on `PYTHONUTF8`, the active PowerShell code page, or a locale change;
those make the run environment part of the inventory contract. Do not decode
with `cp1252`, replace undecodable bytes, or skip the multilingual case. Do not
change production readers, schemas, source hashes, or tests for this failure.

## Focused retry

After the run-script-only edit, repeat the same command from the RUN directory
(`C:/Users/USER/Downloads/test-skill/plans/runs/nckh-upgrade-261006-0850-attempt-01`),
or equivalently:

```text
python -B inventory-integration.py
```

Record the complete exit code and output. The retry should pass the evaluation
case scan and continue through the protected-hash and documentation-link
checks, creating the script's declared outputs. Preserve the original failed
attempt as historical evidence; do not overwrite it or call the failed run
green.

## Status

Status: DONE

Summary: The inventory script is decoding UTF-8 text with Windows `cp1252`
because all six `Path.read_text()` calls omit an encoding. Add explicit
`encoding="utf-8-sig"` to all six reads, then repeat the same run-local command.

Concerns/Blockers: No output was created before the first decode failure. The
inventory checkpoint remains pending until the corrected script exits cleanly.
