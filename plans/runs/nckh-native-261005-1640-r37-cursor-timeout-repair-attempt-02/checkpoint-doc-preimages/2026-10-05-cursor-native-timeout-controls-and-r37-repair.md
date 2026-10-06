# Cursor native timeout controls and r37 repair

## Verified observations

R36 Cursor10 instrumented Read→Read→Write records exact write effect with two native IDs and seven idempotent receipts. Direct11 still fails public-write oracle with Read-only derived receipt; actual failure cause unverified. Direct12 captures selected Read postToolUseFailure with permission_denied and preToolUse5000ms timeout/failClosed; three synthetic local runner executions0.109–0.125s are kept separate from native timing.

Direct13 changes only preToolUse bound to20s plus context/receipt identity isolation; genuine Read pre/post observed, bytes unchanged, artifact QA pending. Direct14 records public Write exact requested bytes and native plan-only Write permission_denied/plan-only-mutation with byte-identical file. Failure12 and all prior5s gaps stay historical. One raw chunk lost after64KB save rejection, deny chunk truncated and collector failures/preimages retained; zero model retries to hide failures.

Every native batch10–14 removes26 owned matching members and has zero final matching/tracked-live processes. Protected global configs unchanged; CLI-owned hashes kept separate and controller direct-write=false. Fresh AGY listing still cannot identify an AGY-owned window; no app input, accepted access/unlock grants retained. Claude model/effort and remaining surface/event/failure/private-mutation matrix pending.

## R37 repair and continuation

Reviewed source config/template/docs change Cursor preToolUse to20s/failClosed=true; other handlers5s. R37 freezes281 pins/three changed pins, canonical hash `629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb`;17 focused config/runner tests pass. Full local pipeline runs fresh; original attempt01 output-directory setup failure happened before suite child start and remains retained. Fresh r37 packaged native retest remains separate from r36 controls.

Plan remains in-progress44/45, phase3 active and native task unchecked. Owner samples bind only exact r29 VI/EN; installed r25/scientific/stable/release remain separate. No controller global config/trust-store direct-write or AgentWiki publication; CLI-owned state hashes are recorded separately.

## Fresh packaged r37 observation

Native15 uses a newly built r37 ON Cursor bundle and producer-default preToolUse20s, other handlers5s. Two turns verify exact public Write bytes and actual native plan-only Write permission_denied/plan-only-mutation with unchanged bytes. Final markers/Stop observed; earlier running deny record kept before terminal reconciliation, zero prompt retries. Raw terminal chunks truncated and actual policy/effect bindings verified separately. Matching cleanup removes26 members, preserves626 historical members, final audit zero. Protected configs unchanged, CLI-owned state hash changes and controller direct-write=false. R37 suite192 tests successful with one Windows symlink skip; package stages continue.

> Historical work record; current authority remains the owning docs/source and revision-bound receipts.
