"""Negotiate installed parameter selectors before allowing any inference."""

import importlib.util
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
BASE = WORK / "plans/runs/nckh-native-261005-1109-r36-cursor-acp-attempt-01"
spec = importlib.util.spec_from_file_location("acp_parameter_metadata_base", BASE / "cursor-acp-client.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
probe.RUN = RUN
EXPECTED_OPTIONS = {"model": "grok-4.7", "context": "500k", "reasoning_effort": "xhigh", "fast": "false"}


class ParameterClient(probe.Client):
    def request(self, method, params, timeout):
        if method == "initialize":
            params = json.loads(json.dumps(params))
            params["clientCapabilities"]["_meta"] = {"parameterizedModelPicker": True}
        answer = super().request(method, params, timeout)
        if method != "session/new" or answer.get("error"):
            return answer
        sid = answer["result"]["sessionId"]
        options = answer["result"].get("configOptions", [])
        record = {"status": "configuring-native-parameters-no-inference", "native_session": answer,
            "expected_options": EXPECTED_OPTIONS, "responses": [], "model_turns": 0,
            "model_requested": probe.MODEL, "source_revision": 36, "source_lock_hash": probe.EXPECTED,
            "client_meta": {"parameterizedModelPicker": True}, "source_modified": False}
        probe.atomic_json(RUN / "parameter-selector-result.json", record)
        for identifier, value in EXPECTED_OPTIONS.items():
            option = next((item for item in options if item["id"] == identifier), None)
            assert option is not None, "Native session did not expose requested parameter: " + identifier
            supported = [item["value"] for item in option["options"]]
            assert value in supported, "Requested value is not advertised by native host: " + identifier
            if option["currentValue"] == value:
                continue
            configured = super().request("session/set_config_option", {
                "sessionId": sid, "configId": identifier, "value": value}, timeout=45)
            record["responses"].append({"config_id": identifier, "value": value, "native_response": configured})
            probe.atomic_json(RUN / "parameter-selector-result.json", record)
            assert not configured.get("error"), "Native host rejected the granted parameter: " + identifier
            options = configured["result"]["configOptions"]
        current = {item["id"]: item["currentValue"] for item in options}
        record["final_native_options"] = current
        record["exact_granted_parameters_verified"] = all(current.get(k) == v for k, v in EXPECTED_OPTIONS.items())
        record["status"] = "verified-exact-native-model-parameters" if record["exact_granted_parameters_verified"] else "exact-parameters-unverified-no-inference"
        probe.atomic_json(RUN / "parameter-selector-result.json", record)
        print(json.dumps({"parameter_status": record["status"], "model_turns": 0,
            "final_native_options": current}), flush=True)
        assert record["exact_granted_parameters_verified"], "Model parameters differ from the human grant"
        return answer


if __name__ == "__main__":
    source = Path(r"C:/Users/USER\AppData\Local\cursor-agent\versions\2026.09.15-d2fe57e\9646.index.js")
    native_source = source.read_text(encoding="utf8")
    symbols = ("clientSupportsParameterizedModelPicker()", "parameterizedModelPicker",
        "applyParameterizedModelConfigOption(e,t)", "buildParameterizedModelConfigOptions")
    assert all(symbol in native_source for symbol in symbols)
    probe.atomic_json(RUN / "installed-protocol-evidence.json", {
        "source_path": str(source), "source_sha256": probe.digest_file(source),
        "symbol_offsets": {symbol: native_source.index(symbol) for symbol in symbols},
        "scope": "Read-only installed protocol trace; native responses must verify actual behavior",
        "controller_sha256": probe.digest_file(Path(__file__)), "base_controller_sha256": probe.digest_file(BASE / "cursor-acp-client.py")})
    probe.Client = ParameterClient
    probe.metadata()
