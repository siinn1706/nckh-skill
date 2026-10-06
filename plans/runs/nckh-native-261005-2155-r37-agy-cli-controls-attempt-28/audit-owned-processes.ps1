param([Parameter(Mandatory=$true)][ValidateSet('preflight','admission','final')][string]$Stage)
$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskWork = Split-Path (Split-Path (Split-Path $taskRun -Parent) -Parent) -Parent
$taskProject = Join-Path $taskWork 'plans\runs\nckh-native-261005-0005-r34-attempt-01\projects\agy-model'
$taskPrior = Get-Content -LiteralPath (Join-Path $taskWork 'plans\runs\nckh-native-261005-2125-r37-cursor-Write-faults-attempt-27\final-process-audit-attempt-02.json') -Raw | ConvertFrom-Json
$taskAll = @(Get-CimInstance Win32_Process)
$taskExpected = @{}
foreach ($taskRow in $taskPrior.tracked) {
    $taskTicks = ([DateTimeOffset]::Parse($taskRow.expected)).UtcDateTime.ToFileTimeUtc()
    $taskExpected[([string]$taskRow.pid)+':'+$taskTicks] = [pscustomobject]@{pid=$taskRow.pid; creation_filetime_ticks=$taskTicks}
}
foreach ($taskFile in @(Get-ChildItem -LiteralPath (Join-Path $taskRun 'commands') -Filter '*.process-tree.json' -File -ErrorAction SilentlyContinue)) {
    $taskTree = Get-Content -LiteralPath $taskFile.FullName -Raw | ConvertFrom-Json
    foreach ($taskRow in $taskTree.processes) {
        $taskExpected[([string]$taskRow.pid)+':'+$taskRow.creation_filetime_ticks] = $taskRow
    }
}
$taskTracked = @(foreach ($taskExpectedRow in $taskExpected.Values) {
    $taskCurrent = @($taskAll | Where-Object ProcessId -eq $taskExpectedRow.pid)
    $taskSame = $taskCurrent.Count -gt 0 -and $taskCurrent[0].CreationDate.ToUniversalTime().ToFileTimeUtc() -eq $taskExpectedRow.creation_filetime_ticks
    [pscustomobject]@{pid=$taskExpectedRow.pid;creation_filetime_ticks=$taskExpectedRow.creation_filetime_ticks;same_process_live=$taskSame;reused_pid=$taskCurrent.Count -gt 0 -and -not $taskSame}
})
$taskAncestors = @($PID)
$taskAncestor = $PID
while ($true) {
    $taskParent = @($taskAll | Where-Object ProcessId -eq $taskAncestor)
    if ($taskParent.Count -ne 1 -or $taskParent[0].ParentProcessId -eq 0 -or $taskAncestors -contains $taskParent[0].ParentProcessId) {break}
    $taskAncestor = $taskParent[0].ParentProcessId
    $taskAncestors += $taskAncestor
}
$taskMatches = @($taskAll | Where-Object {
    $taskAncestors -notcontains $_.ProcessId -and $_.CommandLine -and
    ($_.CommandLine.Contains($taskRun) -or $_.CommandLine.Contains($taskProject))
} | ForEach-Object { [pscustomobject]@{pid=$_.ProcessId;name=$_.Name;creation_utc=$_.CreationDate.ToUniversalTime().ToString('o')} })
$taskRecord = [ordered]@{timestamp_utc=[datetime]::UtcNow.ToString('o');stage=$Stage;project=$taskProject;matching_count=$taskMatches.Count;matches=$taskMatches;tracked_live_count=@($taskTracked | Where-Object same_process_live).Count;tracked=$taskTracked;process_stop_performed=$false;identity_source='prior native27 audit plus exact Win32 process creation FILETIME captures';excluded_ancestor_pids=$taskAncestors}
$taskTarget = Join-Path $taskRun ('process-'+$Stage+'-audit.json')
if (Test-Path -LiteralPath $taskTarget) {throw 'Preserve existing audit'}
$taskRecord | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
[pscustomobject]@{stage=$Stage;matching_count=$taskMatches.Count;tracked_live_count=$taskRecord.tracked_live_count;tracked_count=$taskTracked.Count} | ConvertTo-Json
if ($taskRecord.matching_count -ne 0 -or $taskRecord.tracked_live_count -ne 0) {throw 'Owned process still live; reconcile before dependent work'}
