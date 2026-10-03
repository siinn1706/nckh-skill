#!/bin/sh
set -eu
if command -v python3 >/dev/null 2>&1; then
    nckh_python=python3
elif command -v python >/dev/null 2>&1; then
    nckh_python=python
else
    echo 'Python 3.11+ is required. Install it separately; NCKH never downloads Python.' >&2
    exit 2
fi
if ! "$nckh_python" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 2)'; then
    echo 'Python 3.11+ is required.' >&2
    exit 2
fi
nckh_script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "$nckh_python" "$nckh_script_dir/nckh-installer.py" "$@"
