param([Parameter(ValueFromRemainingArguments = $true)][string[]]$InstallerArgs)
$ErrorActionPreference = 'Stop'
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCommand) { $pythonCommand = Get-Command py -ErrorAction SilentlyContinue }
if (-not $pythonCommand) {
    Write-Error 'Python 3.11+ is required. Install it separately; NCKH never downloads Python.'
    exit 2
}
& $pythonCommand.Source -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 2)'
if ($LASTEXITCODE -ne 0) {
    Write-Error 'Python 3.11+ is required.'
    exit 2
}
& $pythonCommand.Source (Join-Path $PSScriptRoot 'nckh-installer.py') @InstallerArgs
exit $LASTEXITCODE
