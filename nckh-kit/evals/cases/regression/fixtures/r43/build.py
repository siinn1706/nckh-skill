import hashlib
from pathlib import Path
print(hashlib.sha256(Path("app.py").read_bytes()).hexdigest())
