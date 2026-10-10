# Visual purpose and asset boundary

## Purpose preflight

Before a controlled generator writes an image or calls a provider, require a
bounded `visual_purpose` in the [brief](../contracts/brief.schema.json): research
question, object, artifact role, evidence IDs/access, origin and mark mapping. A
domain word such as "research" alone is insufficient. A missing, invalid, pending
or denied preflight stops generation. Charts, scientific mechanisms and research
illustrations belong to nckh-visuals. Current generating bindings are
instruction-only/manual/not-callable; a manual check or post-render receipt does
not prove native prevention.

Validator: `core.guards.check_visual_purpose` (run by the hook policy) checks the purpose; `check-visual-engine.py` checks a task-supplied engine binding.

## Marketing and brand assets

Logos (including research logos), banners, ads, thumbnails, social images and
generic artwork are delivered as a written brief only: purpose, audience,
message, format and size, mandatory elements, rights of supplied assets and
acceptance checks. A final asset requires a permitted asset engine selected for
the task. The bundled marketing provider contract
(`extensions/providers/marketing/contract.json`) is `unavailable` with
`engine_binding: null`, so stop at the brief and record the asset gate as
`pending`. Do not present a placeholder, stock image or ad-hoc raster as the final
asset, and do not claim a render without a receipt.

Validator: `check-visual-engine.py` returns `unavailable` for the empty bundled binding; the asset gate stays `pending` until a permitted engine leaves a render receipt.
