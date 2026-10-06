param([Parameter(Mandatory=$true)][ValidateSet('preflight','final')][string]$Stage)
$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskWork = Split-Path (Split-Path (Split-Path $taskRun -Parent) -Parent) -Parent
$taskProjects = @(
    (Join-Path $taskWork 'plans\runs\nckh-native-261005-0128-r34-cursor-events-attempt-02\projects\main'),
    (Join-Path $taskWork 'plans\runs\nckh-native-261005-0005-r34-attempt-01\projects\agy-model')
)
$taskPrior = Get-Content -LiteralPath (Join-Path $taskWork 'plans\runs\nckh-native-261006-0010-r37-agy-shell-control-attempt-38\process-final-audit.json') -Raw | ConvertFrom-Json
$taskExpected = @{}
foreach ($taskRow in $taskPrior.tracked) {
    $taskExpected[([string]$taskRow.pid)+':'+$taskRow.creation_filetime_ticks] = $taskRow
}
foreach ($taskFile in @(Get-ChildItem -LiteralPath (Join-Path $taskRun 'commands') -Filter '*.process-tree.json' -File -ErrorAction SilentlyContinue)) {
    $taskTree = Get-Content -LiteralPath $taskFile.FullName -Raw | ConvertFrom-Json
    foreach ($taskRow in $taskTree.processes) {
        $taskExpected[([string]$taskRow.pid)+':'+$taskRow.creation_filetime_ticks] = $taskRow
    }
}
foreach ($taskFile in @(Get-ChildItem -LiteralPath $taskRun -Filter 'process-tree-*.json' -File)) {
    $taskTree = Get-Content -LiteralPath $taskFile.FullName -Raw | ConvertFrom-Json
    foreach ($taskRow in $taskTree.processes) {
        $taskTicks = ([datetime]$taskRow.creation_utc).ToUniversalTime().ToFileTimeUtc()
        $taskExpected[([string]$taskRow.ProcessId)+':'+$taskTicks] = [pscustomobject]@{pid=$taskRow.ProcessId;creation_filetime_ticks=$taskTicks}
    }
}
$taskAll = @(Get-CimInstance Win32_Process)
$taskAncestors = @($PID)
$taskAncestor = $PID
while ($true) {
    $taskParent = @($taskAll | Where-Object ProcessId -eq $taskAncestor)
    if ($taskParent.Count -ne 1 -or $taskParent[0].ParentProcessId -eq 0 -or $taskAncestors -contains $taskParent[0].ParentProcessId) {break}
    $taskAncestor = $taskParent[0].ParentProcessId
    $taskAncestors += $taskAncestor
}
$taskMatches = @($taskAll | Where-Object {
    if ($taskAncestors -contains $_.ProcessId -or -not $_.CommandLine) {return $false}
    if ($_.CommandLine.Contains($taskRun)) {return $true}
    foreach ($taskProject in $taskProjects) {if ($_.CommandLine.Contains($taskProject)) {return $true}}
    return $false
} | ForEach-Object { [pscustomobject]@{pid=$_.ProcessId;name=$_.Name;creation_utc=$_.CreationDate.ToUniversalTime().ToString('o')} })
$taskTracked = @(foreach ($taskRow in $taskExpected.Values) {
    $taskCurrent = @($taskAll | Where-Object ProcessId -eq $taskRow.pid)
    $taskSame = $taskCurrent.Count -gt 0 -and $taskCurrent[0].CreationDate.ToUniversalTime().ToFileTimeUtc() -eq $taskRow.creation_filetime_ticks
    [pscustomobject]@{pid=$taskRow.pid;creation_filetime_ticks=$taskRow.creation_filetime_ticks;same_process_live=$taskSame;reused_pid=$taskCurrent.Count -gt 0 -and -not $taskSame}
})
$taskRecord = [ordered]@{timestamp_utc=[datetime]::UtcNow.ToString('o');stage=$Stage;matching_count=$taskMatches.Count;matches=$taskMatches;tracked_live_count=@($taskTracked | Where-Object same_process_live).Count;tracked=$taskTracked;process_stop_performed=$false;excluded_ancestor_pids=$taskAncestors}
$taskTarget = Join-Path $taskRun ('process-'+$Stage+'-audit.json')
if (Test-Path -LiteralPath $taskTarget) {throw 'Preserve existing audit'}
$taskRecord | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
[pscustomobject]@{stage=$Stage;matching_count=$taskMatches.Count;tracked_live_count=$taskRecord.tracked_live_count;tracked_count=$taskTracked.Count} | ConvertTo-Json
if ($taskRecord.matching_count -ne 0 -or $taskRecord.tracked_live_count -ne 0) {throw 'Owned process still live; reconcile before dependent work'}
