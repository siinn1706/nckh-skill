param([Parameter(Mandatory=$true)][ValidateSet('before-launch','after-launch')][string]$Stage)
$ErrorActionPreference = 'Stop'
$taskRows = @(Get-CimInstance Win32_Process -Filter "Name = 'Antigravity.exe'" | ForEach-Object {
    [pscustomobject]@{pid=$_.ProcessId; parent_pid=$_.ParentProcessId; name=$_.Name; executable=$_.ExecutablePath; creation_utc=$_.CreationDate.ToUniversalTime().ToString('o')}
})
$taskRecord = [ordered]@{timestamp_utc=[datetime]::UtcNow.ToString('o'); stage=$Stage; processes=$taskRows; app_input_sent=$false; process_stop_performed=$false}
$taskPath = Join-Path $PSScriptRoot ('agy-process-' + $Stage + '.json')
if (Test-Path -LiteralPath $taskPath) { throw 'Preserve existing process snapshot' }
$taskRecord | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $taskPath -Encoding utf8NoBOM
[pscustomobject]@{stage=$Stage; count=$taskRows.Count; roots=@($taskRows | Where-Object { $taskRows.pid -notcontains $_.parent_pid } | Select-Object pid,creation_utc)} | ConvertTo-Json -Depth 4
