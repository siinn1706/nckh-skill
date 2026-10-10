#!/bin/sh
set -eu
nckh_script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
nckh_script="$nckh_script_dir/nckh-installer.py"
case "$(uname -s)" in
    MSYS*|MINGW*|CYGWIN*) nckh_script=$(cygpath -w "$nckh_script") ;;
esac
nckh_probe='import sys; from pathlib import Path; p=Path(sys.executable); sys.exit(2) if sys.version_info < (3, 11) else None; p.read_bytes(); print(sys.executable)'
if [ -n "${NCKH_PYTHON:-}" ]; then
    if nckh_executable=$("$NCKH_PYTHON" -c "$nckh_probe" 2>/dev/null); then
        echo "NCKH Python: $nckh_executable" >&2
        exec "$NCKH_PYTHON" "$nckh_script" "$@"
    fi
else
    for nckh_python in python3 python py; do
        if ! command -v "$nckh_python" >/dev/null 2>&1; then continue; fi
        if [ "$nckh_python" = py ]; then
            if nckh_executable=$(py -3 -c "$nckh_probe" 2>/dev/null); then
                echo "NCKH Python: $nckh_executable" >&2
                exec py -3 "$nckh_script" "$@"
            fi
        elif nckh_executable=$("$nckh_python" -c "$nckh_probe" 2>/dev/null); then
            echo "NCKH Python: $nckh_executable" >&2
            exec "$nckh_python" "$nckh_script" "$@"
        fi
    done
fi
echo 'Python 3.11+ with a readable executable is required. Set NCKH_PYTHON to a real interpreter path. NCKH never downloads Python.' >&2
exit 2
