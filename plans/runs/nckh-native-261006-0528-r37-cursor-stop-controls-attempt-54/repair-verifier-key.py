"""Repair a generated mapping key after proving its unary-plus type error."""
import ast
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
WORK = RUN.parents[2]
target = RUN / "verify-stop-observations.py"
bootstrap = RUN / "prepare-controller.py"
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
bind = lambda path: {"path":path.relative_to(WORK).as_posix(),"sha256":sha(path)}
source = target.read_text(encoding="utf8")
nodes = [node for node in ast.walk(ast.parse(source)) if isinstance(node,ast.UnaryOp)
    and isinstance(node.op,ast.UAdd) and isinstance(node.operand,ast.Constant) and isinstance(node.operand.value,str)]
assert len(nodes) == 1 and nodes[0].operand.value == "repeat_behavior"
try:
    eval(compile(ast.Expression(nodes[0]),str(target),"eval"),{"__builtins__":{}})
except TypeError as error:
    actual_error = type(error).__name__+": "+str(error)
else:
    raise AssertionError("Expected mapping-key failure was not reproduced")
preimages = []
for path,name in ((target,"verifier-key-preimage.py"),(bootstrap,"controller-key-preimage.py")):
    preimage = RUN / name
    with preimage.open("xb") as stream:
        stream.write(path.read_bytes())
    preimages.append(bind(preimage))
needle = '\n+    "repeat_behavior"'
assert source.count(needle) == 1
source = source.replace(needle,'\n    "repeat_behavior"')
bootstrap_source = bootstrap.read_text(encoding="utf8")
needle = r'\n+    "repeat_behavior"'
assert bootstrap_source.count(needle) == 1
bootstrap_source = bootstrap_source.replace(needle,r'\n    "repeat_behavior"')
compile(source,str(target),"exec")
compile(bootstrap_source,str(bootstrap),"exec")
target.write_text(source,encoding="utf8",newline="\n")
bootstrap.write_text(bootstrap_source,encoding="utf8",newline="\n")
record = {"status":"fixed-proven-generated-mapping-key-error-before-native-model", "actual_error":actual_error,
    "line":nodes[0].lineno,"preimages":preimages,"after":[bind(target),bind(bootstrap)],
    "byte_content_oracles_changed":False,"native_definitions_changed":False,"source_kit_modified":False,"model_prompts":0}
with (RUN / "verifier-key-repair.json").open("x",encoding="utf8",newline="\n") as stream:
    stream.write(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":record["status"],"actual_error":actual_error,"model_prompts":0}))
