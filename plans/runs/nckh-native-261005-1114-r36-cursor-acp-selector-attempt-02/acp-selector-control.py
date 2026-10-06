"""Verify the exact model variant through the native session configuration API."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1109-r36-cursor-acp-attempt-01"
spec = importlib.util.spec_from_file_location("acp_selector_metadata_base", BASE / "cursor-acp-client.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.RUN = RUN


class SelectorClient(probe.Client):
    def request(self, method, params, timeout):
        answer = super().request(method, params, timeout)
        if method == "session/new" and not answer.get("error"):
            result = answer["result"]
            initial = next((item["currentValue"] for item in result.get("configOptions", [])
                if item["id"] == "model"), None)
            configured = super().request("session/set_config_option", {
                "sessionId": result["sessionId"], "configId": "model", "value": probe.MODEL}, timeout=45)
            options = configured.get("result", {}).get("configOptions", [])
            current = next((item["currentValue"] for item in options if item["id"] == "model"), None)
            record = {"status": "verified-exact-native-model-selector" if current == probe.MODEL else "exact-selector-unverified-no-inference",
                "model_requested": probe.MODEL, "initial_native_model": initial,
                "configured_native_model": current, "native_response": configured,
                "native_session": answer, "model_turns": 0, "source_revision": 36,
                "source_lock_hash": probe.EXPECTED, "source_modified": False,
                "controller": {"path": Path(__file__).relative_to(WORK).as_posix(),
                    "sha256": probe.digest_file(Path(__file__))},
                "base_controller": {"path": (BASE / "cursor-acp-client.py").relative_to(WORK).as_posix(),
                    "sha256": probe.digest_file(BASE / "cursor-acp-client.py")}}
            probe.atomic_json(RUN / "model-selector-result.json", record)
            print(json.dumps({"selector_status": record["status"], "model_turns": 0,
                "configured_native_model": current}), flush=True)
            if current != probe.MODEL:
                raise RuntimeError("Exact native model selector is unverified; no inference submitted")
        return answer


if __name__ == "__main__":
    probe.Client = SelectorClient
    probe.metadata()
