"""Verify retained native evidence without regrading failures or replaying callbacks."""
import hashlib,json,sys
from pathlib import Path
from collections import Counter
WORK=Path(r"C:/Users/USER\Downloads\test-skill")
RUN=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(WORK/"nckh-kit"))
from core.build import verify_source_lock
from core.paths import digest_record,contained
EXPECTED="4482bbba7f4537025b523d887abe34774a4427d397549730f1ba8cf9fd50a255"
assert digest_record(verify_source_lock(WORK/"nckh-kit"))==EXPECTED
read=lambda p:json.loads(p.read_text(encoding="utf-8-sig"))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bind=lambda p:{"path":p.relative_to(WORK).as_posix(),"sha256":sha(p)}
NAMES=["nckh-native-261005-0746-r35-cursor-file-attempt-01","nckh-native-261005-0812-r35-cursor-write-faults-attempt-01",
 "nckh-native-261005-0822-r35-cursor-write-faults-attempt-02","nckh-native-261005-0818-r35-cursor-template-timing-attempt-01"]
rows=[];components=[]
for name in NAMES:
 root=WORK/"plans/runs"/name
 summary=read(root/"native-file-summary.json")
 stage=read(root/"stage.json")
 project=Path(stage["preview"]["project"])
 assert stage["source_lock_hash"]==EXPECTED and len(stage["staged_members"])==25
 cleanup=read(root/"cleanup.json")
 audit=read(root/"final-process-audit.json")
 assert cleanup["status"]==audit["status"]=="pass" and audit["count"]==0 and not cleanup["config_callable"]
 assert all(r["sha256"]==r["current_sha256"] for r in cleanup["protected_global_config"])
 assert not (project/".cursor/hooks.json").exists()
 for member in cleanup["removed_members"]:assert not contained(project,member["path"]).exists()
 component={"run":name,"summary":bind(root/"native-file-summary.json"),"stage":bind(root/"stage.json"),
  "metadata":bind(root/"native-metadata.json"),"ownership":bind(root/"ownership.json"),"cleanup":bind(root/"cleanup.json"),
  "process_audit":bind(root/"final-process-audit.json"),"removed_members":len(cleanup["removed_members"]),
  "historical_members_preserved":cleanup["historical_members_unchanged"],
  "global_cli_hash_changed":cleanup["global_cli_hash_before"]!=cleanup["global_cli_hash_after"]}
 if (root/"terminal-reconciliation.json").exists():component["terminal_reconciliation"]=bind(root/"terminal-reconciliation.json")
 components.append(component)
 for entry in summary["results"]:
  path=WORK/entry["receipt"]["path"]
  assert sha(path)==entry["receipt"]["sha256"]
  r=read(path)
  assert r["source_lock_hash"]==EXPECTED and r["process_exited"] and r["exit_code"]==0
  command=WORK/r["command_receipt"]["path"]
  assert sha(command)==r["command_receipt"]["sha256"]
  c=read(command)
  assert c["process_exited"] and c["exit_code"]==0 and c["status"]=="completed"
  assert c["command"][c["command"].index("--model")+1]=="grok-4.7[context=500k,reasoning_effort=xhigh,fast=false]"
  stem=command.with_suffix("")
  stdout=Path(str(stem)+".stdout.txt");stderr=Path(str(stem)+".stderr.txt")
  assert sha(stdout)==c["stdout_sha256"] and sha(stderr)==c["stderr_sha256"]
  frames=[json.loads(line) for line in stdout.read_text(encoding="utf8").splitlines()]
  completed=[f for f in frames if f.get("type")=="tool_call" and f.get("subtype")=="completed"]
  assert completed==r["completed_tool_calls"] and len(completed)==1
  definition=WORK/r["definition"]["path"]
  assert sha(definition)==r["definition"]["sha256"]
  callbacks=r.get("native_callbacks",[])
  for binding in r.get("callback_bindings",[]):assert sha(WORK/binding["path"])==binding["sha256"]
  pretool=sorted([b for b in callbacks if b["event"]=="preToolUse"],key=lambda b:b["started_at"])
  call=completed[0]["tool_call"];outer=next(k for k in ("editToolCall","readToolCall","shellToolCall") if k in call)
  native_result=call[outer].get("result",{})
  result_kind=next(iter(native_result))
  actual_path=contained(project,r["path"])
  current=sha(actual_path) if actual_path.is_file() else None
  assert current==r["after_sha256"]
  policies=[]
  for p in r["policy_receipts"]:
   pp=WORK/p["path"];assert sha(pp)==p["sha256"]
   data=read(pp);policies.append({"binding":bind(pp),"decision":data["decision"],"reasons":data["reason_codes"],"phase":data.get("phase"),"event_hash":data.get("event_hash")})
  callback_rows=[{k:b.get(k) for k in ("native_tool_name","native_tool_use_id","callback_source","started_at","completed_at",
   "fault_selected","fault_origin","fault_target_tool","status","runner_exit_code","native_path_fields")} for b in pretool]
  rows.append({"run":name,"attempt":r["attempt"],"kind":r["kind"],"mode":r["mode"],"before_sha256":r["before_sha256"],
   "after_sha256":r["after_sha256"],"marker_present":r["file_exists"],"outer_tool":outer,"outer_result":result_kind,
   "outer_tool_id":call["toolCallId"],"native_result":native_result,"callbacks":callback_rows,"policies":policies,
   "events_observed":sorted(set(b["event"] for b in callbacks)),"receipt":bind(path),"command":bind(command),"stdout":bind(stdout),
   "stderr":bind(stderr),"definition":bind(definition),"fault_origin":r["fault_origin"],"timeout_seconds":r.get("timeout_seconds"),
   "observer_invoked":r.get("observer_invoked",True)})
by={r["attempt"]:r for r in rows}
for attempt in ("write-allow","write-uncovered","write-duplicate"):
 r=by[attempt];assert r["outer_result"]=="success" and r["marker_present"]
 assert r["after_sha256"]==hashlib.sha256(b"NCKH_CURSOR_FILE_ORACLE\n").hexdigest()
for attempt in ("write-policy-deny","write-private"):
 assert not by[attempt]["marker_present"] and by[attempt]["outer_result"] in {"error","rejected"}
assert [b["native_tool_name"] for b in by["write-policy-deny"]["callbacks"]]==["Read","Write"]
assert [b["native_tool_name"] for b in by["write-private"]["callbacks"]]==["Read"]
for attempt in ("read-allow","read-private"):
 assert by[attempt]["before_sha256"]==by[attempt]["after_sha256"]
assert by["read-allow"]["outer_result"]=="success" and by["read-private"]["outer_result"]=="error"
dup=by["write-duplicate"]
assert Counter((b["native_tool_name"],b["callback_source"]) for b in dup["callbacks"])==Counter({("Read","project"):1,("Read","plugin"):1,("Write","project"):1,("Write","plugin"):1})
assert len(set(b["native_tool_use_id"] for b in dup["callbacks"]))==1 and len(dup["policies"])==2
original_faults=[by["write-"+mode] for mode in ("malformed-input","malformed-output","timeout","crash","unsupported-codec")]
assert all(len(r["callbacks"])==1 and r["callbacks"][0]["native_tool_name"]=="Read" and not r["marker_present"] for r in original_faults)
qualified=[by["write-stage-malformed-input"],by["write-stage-malformed-output"],by["write-stage-02-timeout"],by["write-stage-02-crash"],by["write-stage-02-unsupported-codec"]]
assert len({r["mode"] for r in qualified})==5
for r in qualified:
 selected=[b for b in r["callbacks"] if b["fault_selected"]]
 assert len(selected)==1 and selected[0]["native_tool_name"]=="Write" and not r["marker_present"] and r["outer_result"]=="error"
 assert all(not b["fault_selected"] for b in r["callbacks"] if b["native_tool_name"]=="Read")
interrupted=by["write-stage-timeout"]
assert len(interrupted["callbacks"])==1 and not interrupted["callbacks"][0]["fault_selected"] and interrupted["outer_result"]=="rejected"
timing=by["template-write-allow"]
assert not timing["marker_present"] and timing["outer_result"]=="rejected" and not timing["observer_invoked"] and timing["timeout_seconds"]==5
assert "5000ms" in json.dumps(timing["native_result"]) and any(p["decision"]=="allow" for p in timing["policies"])
result={"status":"recorded-cursor-file-and-write-fault-observations-template-timing-failed","source_revision":35,"source_lock_hash":EXPECTED,
 "native_turns":len(rows),"baseline_turns":6,"original_read_stage_faults":5,"direct_write_stage_faults":5,"duplicate_turns":1,
 "interrupted_write_fault_turns":1,"direct_template_timing_turns":1,"components":components,"attempts":rows,
 "qualified_write_fault_attempts":[r["attempt"] for r in qualified],"full_native_gate":"open","native_checkbox":"unchecked",
 "timing_qualification":"failed-5-second-native-direct-runner","timeout_root_cause":"unresolved",
 "source_changes":"none","independent_review":"not-run; inline review","backend_attestation":"not-observed","billing":"not-observed",
 "claims_limit":"One outer edit can emit Read and Write callbacks with the same ID. Original fault batch failed at Read; qualified supplemental faults selected Write only. Unknown codec injection is not native unsupported-tool evidence.",
 "remaining":["CLI prompt and stop callbacks","intermittent native timeout diagnosis","other tool routes","direct IDE receipts","full four-host event/version/surface task"]}
output=WORK/"plans/reports/delivery-261005-0746-r35-cursor-files.json"
assert not output.exists()
output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
print(json.dumps({"status":result["status"],"turns":len(rows),"direct_write_faults":5,"read_stage_faults":5,"removed_matching_members":sum(c["removed_members"] for c in components),"template_timing":"failed","full_native_gate":"open"}))
