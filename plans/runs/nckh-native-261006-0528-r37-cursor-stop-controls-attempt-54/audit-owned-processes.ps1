param([Parameter(Mandatory=$true)][ValidateSet('preflight','final')][string]$Stage)
$ErrorActionPreference = 'Stop'
$taskRun=$PSScriptRoot
$taskWork=Split-Path (Split-Path (Split-Path $taskRun -Parent) -Parent) -Parent
$taskProject=Join-Path $taskWork 'plans\runs\nckh-native-261005-0128-r34-cursor-events-attempt-02\projects\main'
$taskPriorPath=Join-Path $taskWork 'plans\runs\nckh-native-261006-0453-r37-cursor-posttool-lf-controls-attempt-53\process-final-audit.json'
$taskPrior=Get-Content -LiteralPath $taskPriorPath -Raw | ConvertFrom-Json
$taskExpected=@{}
foreach ($taskRow in $taskPrior.tracked) {
    $taskKey=([string]$taskRow.pid)+':'+$taskRow.creation_filetime_ticks
    $taskExpected[$taskKey]=$taskRow
}
if ($taskExpected.Count -ne 1542) {throw 'Qualified prior identity set changed'}
if (Test-Path -LiteralPath (Join-Path $taskRun 'commands')) {
    foreach ($taskFile in @(Get-ChildItem -LiteralPath (Join-Path $taskRun 'commands') -Filter '*.process-tree.json' -File)) {
        $taskTree=Get-Content -LiteralPath $taskFile.FullName -Raw | ConvertFrom-Json
        if ($taskTree.capture_errors.Count -ne 0) {throw 'Retained capture errors require reconciliation'}
        foreach ($taskRow in $taskTree.processes) {$taskExpected[([string]$taskRow.pid)+':'+$taskRow.creation_filetime_ticks]=$taskRow}
    }
}
$taskAll=@(Get-CimInstance Win32_Process)
$taskByPid=@{}
foreach ($taskRow in $taskAll) {$taskByPid[[int]$taskRow.ProcessId]=$taskRow}
$taskAncestors=@($PID)
$taskAncestor=$PID
while ($taskByPid.ContainsKey([int]$taskAncestor)) {
    $taskParent=[int]$taskByPid[[int]$taskAncestor].ParentProcessId
    if ($taskParent -eq 0 -or $taskAncestors -contains $taskParent) {break}
    $taskAncestors+=$taskParent
    $taskAncestor=$taskParent
}
$taskMatches=@($taskAll | Where-Object {$taskAncestors -notcontains $_.ProcessId -and $_.CommandLine -and ($_.CommandLine.Contains($taskRun) -or $_.CommandLine.Contains($taskProject))} |
    ForEach-Object {[pscustomobject]@{pid=$_.ProcessId;name=$_.Name;creation_utc=$_.CreationDate.ToUniversalTime().ToString('o')}})
$taskTracked=@(foreach ($taskRow in $taskExpected.Values) {
    $taskCurrent=$taskByPid[[int]$taskRow.pid]
    $taskTicks=if($null -ne $taskCurrent){$taskCurrent.CreationDate.ToUniversalTime().ToFileTimeUtc()}else{$null}
    $taskSame=$null -ne $taskTicks -and [math]::Abs([decimal]$taskTicks-[decimal]$taskRow.creation_filetime_ticks) -le 9
    [pscustomobject]@{pid=$taskRow.pid;creation_filetime_ticks=$taskRow.creation_filetime_ticks;same_process_live=$taskSame;reused_pid=$null -ne $taskCurrent -and -not $taskSame}
})
$taskRecord=[ordered]@{
    timestamp_utc=[datetime]::UtcNow.ToString('o');stage=$Stage;matches=$taskMatches;matching_count=$taskMatches.Count
    tracked=$taskTracked;tracked_live_count=@($taskTracked | Where-Object same_process_live).Count
    prior_temporally_valid_identities=1542;legacy_raw_union=2968;legacy_raw_union_used_as_ownership=$false
    preexisting_apps_preserved=27;identity_comparison='same PID with creation difference <=9 FILETIME ticks for CIM precision'
    process_stop_performed=$false;excluded_ancestor_pids=$taskAncestors
}
$taskTarget=Join-Path $taskRun ('process-'+$Stage+'-audit.json')
if(Test-Path -LiteralPath $taskTarget){throw 'Preserve prior audit'}
$taskRecord | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
[pscustomobject]@{stage=$Stage;matching_count=$taskMatches.Count;tracked_live_count=$taskRecord.tracked_live_count;qualified_identities=$taskTracked.Count} | ConvertTo-Json
if($taskRecord.matching_count -ne 0 -or $taskRecord.tracked_live_count -ne 0){throw 'Reconcile owned process before dependent work'}
