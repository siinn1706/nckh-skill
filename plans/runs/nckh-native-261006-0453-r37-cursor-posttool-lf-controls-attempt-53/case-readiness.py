"""Read callback completion metadata only; the collector owns all acceptance checks."""
import argparse
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
read = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
parser = argparse.ArgumentParser()
parser.add_argument("--index", type=int, choices=range(1,8), required=True)
args = parser.parse_args()
frozen = read(RUN / "frozen-brief.json")
case = frozen["cases"][args.index-1]
project = Path(frozen["project"])
evidence = project / ".nckh-native-r37-cursor-posttool-lf-controls-53"
callbacks = [read(path) for path in sorted((evidence / "observations" / case["attempt"]).glob("*/*.json"))]
stop = [row for row in callbacks if row["event"] == "stop"]
print(json.dumps({"case":args.index,"mode":case["mode"],"callbacks":len(callbacks),
    "stop_completed":len(stop) == 1 and stop[0]["status"] == "completed",
    "events":[{"event":row["event"],"status":row["status"]} for row in callbacks]}))
