"""Observe the selected callback's actual process state before collecting any outcome."""
import argparse
import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
spec = importlib.util.spec_from_file_location("selected_callback_state",RUN / "native-process-state.py")
states = importlib.util.module_from_spec(spec)
spec.loader.exec_module(states)
parser = argparse.ArgumentParser()
parser.add_argument("--index",type=int,choices=range(1,8),required=True)
args = parser.parse_args()
frozen = read(RUN / "frozen-brief.json")
case = frozen["cases"][args.index-1]
project = Path(frozen["project"])
evidence = project / ".nckh-native-r37-cursor-stop-controls-54"
callbacks = [read(path) for path in sorted((evidence / "observations" / case["attempt"]).glob("*/*.json"))]
stops = [row for row in callbacks if row["event"] == "stop"]
observed = []
for row in stops:
    for pid_key,ticks_key in (("observer_pid","observer_creation_filetime_ticks"),("runner_pid","runner_creation_filetime_ticks")):
        if row.get(pid_key):
            expected = row.get(ticks_key)
            assert expected is not None, "Selected callback generation is missing"
            current = states.state(row[pid_key])
            assert current["status"] != "unobservable", "Selected callback state is unobservable"
            observed.append({**current,"expected_creation_ticks":expected,
                "same_active":current["status"] == "active" and current["creation_filetime_ticks"] == expected})
print(json.dumps({"case":args.index,"mode":case["mode"],"callbacks":len(callbacks),"Stop_count":len(stops),
    "stop_terminal":bool(stops) and bool(observed) and not any(row["same_active"] for row in observed),
    "selected_process_states":observed,"events":[{"event":row["event"],"status":row["status"]} for row in callbacks]}))
