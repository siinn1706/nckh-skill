param([Parameter(ValueFromRemainingArguments = $true)][string[]]$InstallerArgs)
$ErrorActionPreference = 'Stop'
$candidates = @()
if ($env:NCKH_PYTHON) {
    $candidates += @{ Path = $env:NCKH_PYTHON; Prefix = @(); Override = $true }
} else {
    foreach ($command in @(Get-Command python -All -CommandType Application -ErrorAction SilentlyContinue)) {
        $candidates += @{ Path = $command.Source; Prefix = @(); Override = $false }
    }
    $launcher = Get-Command py -CommandType Application -ErrorAction SilentlyContinue
    if ($launcher) { $candidates += @{ Path = $launcher.Source; Prefix = @('-3'); Override = $false } }
}
$probe = 'import sys; from pathlib import Path; p=Path(sys.executable); sys.exit(2) if sys.version_info < (3, 11) else None; p.read_bytes(); print(sys.executable)'
foreach ($candidate in $candidates) {
    if (-not $candidate.Override -and $candidate.Path -like '*\WindowsApps\*') { continue }
    $prefix = $candidate.Prefix
    try {
        $executable = & $candidate.Path @prefix -c $probe 2>$null
        if ($LASTEXITCODE -ne 0 -or -not $executable) { continue }
    } catch { continue }
    [Console]::Error.WriteLine("NCKH Python: $executable")
    & $candidate.Path @prefix (Join-Path $PSScriptRoot 'nckh-installer.py') @InstallerArgs
    exit $LASTEXITCODE
}
[Console]::Error.WriteLine('Python 3.11+ with a readable executable is required. Set NCKH_PYTHON to a real interpreter path. NCKH never downloads Python.')
exit 2
