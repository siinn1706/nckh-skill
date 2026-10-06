param([Parameter(Mandatory=$true)][ValidateSet('preflight','final')][string]$Stage)
$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskWork = Split-Path (Split-Path (Split-Path $taskRun -Parent) -Parent) -Parent
$taskProject = Join-Path $taskWork 'plans\runs\nckh-native-261005-0658-r34-codex-file-attempt-01\project-02'
$taskPriorPath = Join-Path $taskWork 'plans\runs\nckh-native-261006-0253-r37-codex-posttool-controls-attempt-47\process-final-audit.json'
$taskPrior = Get-Content -LiteralPath $taskPriorPath -Raw | ConvertFrom-Json
$taskExpected = @{}
foreach ($taskRow in $taskPrior.tracked) {
    $taskExpected[([string]$taskRow.pid)+':'+$taskRow.creation_filetime_ticks] = $taskRow
}
if ($taskExpected.Count -ne 2164) {throw 'Unexpected prior process union; inspect before continuing'}
if (Test-Path -LiteralPath (Join-Path $taskRun 'commands')) {
    foreach ($taskFile in @(Get-ChildItem -LiteralPath (Join-Path $taskRun 'commands') -Filter '*.process-tree.json' -File)) {
        $taskTree = Get-Content -LiteralPath $taskFile.FullName -Raw | ConvertFrom-Json
        if ($taskTree.capture_errors.Count -ne 0) {throw 'Retained process capture has errors'}
        foreach ($taskRow in $taskTree.processes) {
            $taskExpected[([string]$taskRow.pid)+':'+$taskRow.creation_filetime_ticks] = $taskRow
        }
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
    $taskAncestors -notcontains $_.ProcessId -and $_.CommandLine -and
    ($_.CommandLine.Contains($taskRun) -or $_.CommandLine.Contains($taskProject))
} | ForEach-Object {[pscustomobject]@{pid=$_.ProcessId;name=$_.Name;creation_utc=$_.CreationDate.ToUniversalTime().ToString('o')}})
$taskTracked = @(foreach ($taskRow in $taskExpected.Values) {
    $taskCurrent = @($taskAll | Where-Object ProcessId -eq $taskRow.pid)
    $taskSame = $taskCurrent.Count -gt 0 -and $taskCurrent[0].CreationDate.ToUniversalTime().ToFileTimeUtc() -eq $taskRow.creation_filetime_ticks
    [pscustomobject]@{pid=$taskRow.pid;creation_filetime_ticks=$taskRow.creation_filetime_ticks;same_process_live=$taskSame;reused_pid=$taskCurrent.Count -gt 0 -and -not $taskSame}
})
$taskRecord = [ordered]@{
    timestamp_utc=[datetime]::UtcNow.ToString('o');stage=$Stage;matching_count=$taskMatches.Count;matches=$taskMatches
    tracked_live_count=@($taskTracked | Where-Object same_process_live).Count;tracked=$taskTracked
    process_stop_performed=$false;excluded_ancestor_pids=$taskAncestors;previous_union_count=2164
}
$taskTarget = Join-Path $taskRun ('process-recovery-'+$Stage+'-audit.json')
if (Test-Path -LiteralPath $taskTarget) {throw 'Preserve existing audit'}
$taskRecord | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
[pscustomobject]@{stage=$Stage;matching_count=$taskMatches.Count;tracked_live_count=$taskRecord.tracked_live_count;tracked_count=$taskTracked.Count} | ConvertTo-Json
if ($taskRecord.matching_count -ne 0 -or $taskRecord.tracked_live_count -ne 0) {throw 'Owned process remains live; reconcile before dependent work'}

