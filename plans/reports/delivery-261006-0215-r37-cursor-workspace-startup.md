# Cursor CLI: genuine workspace/plugin startup route

[Verified native bindings](../runs/nckh-native-261006-0215-r37-cursor-workspace-startup-attempt-43/verified-startup-delivery.json) record a distinct startup-only observation on Cursor CLI 2026.09.15-d2fe57e with the existing Grok4.7/500k/xhigh/fastfalse selection. Zero model prompts and zero tool requests.

One actual workspaceOpen callback returned the owned plugin directory. The CLI then delivered one project and one plugin sessionStart callback with the same input/session hash; unchanged packaged r37 runner returned exit0 and created one idempotent policy receipt. Plugin loading used workspaceOpen output, with no --plugin-dir argument. This proves a scoped native startup route; native42 source inspection alone did not establish that route.

The workspace handler is a controller diagnostic returning pluginPaths. It does not invoke an unsupported packaged codec event. Prompt/stop and tool duplicate pairs remain pending and native19/21 failures retain their original results. Project/plugin provenance is bound to distinct controller-owned command definitions and genuine shared native input.

After readiness, the recorded startup window lasted15 seconds. Native /exit and monitor both ended exit0. Matching cleanup removed32 owned config/payload/helper members and preserved862 historical project files and four new observation/receipt files. Final union1393 process identities had zero matching/tracked-live; no process stop performed. Protected global hook/MCP/plugin config hashes match their preimages. CLI-owned state hashes are recorded without inferring changed fields; controller global direct writes=false.

Source kit r37/281 pins/hash629f056d6686de77a68789843ea78277e1574cdf34152fe7e93f967021ca7fdb is unchanged. Plan stays44/45/P3 active/full native gate unchecked. Native41 test-cache authority and the existing Claude model/effort selection still await direct user answers. Review was inline; no independent reviewer.
