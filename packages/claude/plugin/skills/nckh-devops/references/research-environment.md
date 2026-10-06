# Reproducible research environment

Observe OS/architecture/runtime and selected package versions; bind code/config/data,
workload/model versions and actual commands. Record CPU/GPU/quota/affinity/scheduler,
memory/time/egress/provider limits when observable. Unknown is not unlimited, free or
zero. CPU count alone does not establish effective CPU entitlement or available memory.
Do not install runtimes, contact providers or launch cluster workloads from metadata.

Before a permitted long-running process inspect existing project/port owners. Track
command, PID, creation identity, port and workspace; use deterministic ports and keep
observable handles. Reconcile timeouts/cancellation with actual exit before retry.
Stop only owned matching processes and close handles. Retain failed attempts/stdout/
stderr, exit status, output hashes and exact cleanup receipt. A file's existence does
not establish successful execution. Do not record secrets or complete environment maps.

Cook owns authorized run lifecycle, method owns reproducibility design, dataset owns
split/rights and AIOps/statistics own metrics/readout. Deployment, fault injection,
credential/trust changes and cloud costs keep their separate grants and rollback routes.
Local arithmetic or packaging is distinct from scientific/native/production acceptance.

Use the [research run receipt](_shared/core/contracts/research-run-receipt.schema.json)
and [experiment graph](_shared/core/contracts/experiment-manifest.schema.json)
for actual task observations. The [scoped checker](_shared/scripts/check-research-artifacts.py)
is read-only except its fresh explicit output receipt; it cannot execute recorded
commands or validate a fabricated OS observation. Record launch timestamps and
independent OS creation observations with their actual coverage. No process or
port is implied merely by a manifest entry.
