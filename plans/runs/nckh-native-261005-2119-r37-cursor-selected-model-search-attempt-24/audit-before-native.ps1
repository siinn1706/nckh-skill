param([Parameter(Mandatory=$true)][ValidateSet('prepare','launch')][string]$Stage)
$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskWork = (Resolve-Path -LiteralPath (Join-Path $taskRun '..\..\..')).Path
$taskProject = Join-Path $taskWork 'plans\runs\nckh-native-261005-0128-r34-cursor-events-attempt-02\projects\main'
$taskPrevious = Join-Path $taskWork 'plans\runs\nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21'
$taskProcesses = @(Get-CimInstance Win32_Process)
$taskOldAudit = Get-Content -LiteralPath (Join-Path $taskPrevious 'final-process-audit.json') -Raw | ConvertFrom-Json
$taskTracked = @(foreach ($taskExpected in $taskOldAudit.tracked) {
    $taskActual = @($taskProcesses | Where-Object ProcessId -eq $taskExpected.pid)
    [pscustomobject]@{pid=$taskExpected.pid; expected=$taskExpected.expected; same_process_live=($taskActual.Count -eq 1 -and $taskActual[0].CreationDate.ToUniversalTime().Ticks -eq ([datetime]$taskExpected.expected).ToUniversalTime().Ticks)}
})
$taskMatches = @($taskProcesses | Where-Object {
    if ($_.ProcessId -eq $PID -or !$_.CommandLine -or $_.Name -notmatch '^(?:python(?:w)?|node)\.exe$') { return $false }
    if ($_.Name -eq 'node.exe' -and $_.CommandLine -like '*cursor-agent*' -and $_.CommandLine.Contains($taskProject)) { return $true }
    return $_.CommandLine.Contains($taskRun)
} | ForEach-Object { [pscustomobject]@{pid=$_.ProcessId; parent_pid=$_.ParentProcessId; name=$_.Name; creation_utc=$_.CreationDate.ToUniversalTime().ToString('o')} })
$taskRecord = [ordered]@{timestamp_utc=[datetime]::UtcNow.ToString('o'); matching_count=$taskMatches.Count; matches=$taskMatches; tracked_live_count=@($taskTracked | Where-Object same_process_live).Count; tracked=$taskTracked; project=$taskProject; port=$null; process_stop_performed=$false}
$taskTarget = Join-Path $taskRun $(if ($Stage -eq 'prepare') {'process-preflight.json'} else {'prelaunch-process-audit.json'})
if (Test-Path -LiteralPath $taskTarget) { throw 'Preserve existing process preflight' }
$taskRecord | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
[pscustomobject]@{stage=$Stage; matching_count=$taskRecord.matching_count; tracked_live_count=$taskRecord.tracked_live_count} | ConvertTo-Json
if ($taskRecord.matching_count -ne 0 -or $taskRecord.tracked_live_count -ne 0) { exit 1 }
