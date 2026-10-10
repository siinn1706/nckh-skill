# Evidence and wording

Use source -> evidence -> claim -> synthesis -> prose. Preserve source version/hash,
access level, original context and exact locators. Distinguish identity/status/ranking,
semantic support, methodological validity and human acceptance.

Metadata or an abstract cannot justify unseen methods/results. A real DOI does not
support an unrelated claim. Quote only text actually read; OCR requires a visual
check before exact quotation. Literary sources retain edition, translator, original
language and line/page context. Do not invent missing pages, citations or numbers.

Verdicts: supported permits wording within observed scope; contradicted requires
correction or a documented conflict; insufficient/unverified permits only a bounded
uncertainty statement or marked hypothesis. Never turn uncertainty into fact.
Keep counterevidence and correction/retraction status. Recheck when source/edition,
venue policy, ranking year, notices or task scope changes.

Quartiles require issuer/system, category, metric year, as-of and evidence. Journal
and conference rules remain separate, keyed by venue/year/track/article type.
Public access or OA discovery is not redistribution permission. Human/domain review
is separate from a model critique or deterministic check.

## Attempt status

Every claim record in the [claim schema](../contracts/claim.schema.json) carries an
`attempt_status` from the [Attempt ledger](../workflows/execution.md#attempt-ledger).
A `supported` or `verified-this-attempt` claim needs evidence produced in the
current attempt; an inherited number without a locator in the attempt's inputs is
`unverified` and stays out of factual positions.

Validator: `core.ledger.validate_claim` checks the claim schema and rejects support without evidence.
