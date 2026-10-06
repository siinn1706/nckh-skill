param([Parameter(Mandatory=$true)][ValidateSet('preflight','final')][string]$Stage)
$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskWork = Split-Path (Split-Path (Split-Path $taskRun -Parent) -Parent) -Parent
$taskProject = Join-Path $taskWork 'plans\runs\nckh-native-261005-0128-r34-cursor-events-attempt-02\projects\main'
$taskPaths = @(
    (Join-Path $taskWork 'plans\runs\nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21'),
    (Join-Path $taskWork 'plans\runs\nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24'),
    (Join-Path $taskWork 'plans\runs\nckh-native-261005-2055-r37-cursor-selected-write-attempt-25')
)
if ($Stage -eq 'final') { $taskPaths += $taskRun }
$taskExpected = @{}
foreach ($taskPath in $taskPaths) {
    foreach ($taskName in @('process-tree-start.json','process-tree-before-stop.json')) {
        $taskFile = Join-Path $taskPath $taskName
        if (Test-Path -LiteralPath $taskFile) {
            $taskTree = Get-Content -LiteralPath $taskFile -Raw | ConvertFrom-Json
            foreach ($taskRow in $taskTree.processes) {
                $taskKey = ([string]$taskRow.ProcessId) + ':' + ([datetime]$taskRow.creation_utc).ToUniversalTime().Ticks
                $taskExpected[$taskKey] = $taskRow
            }
        }
    }
}
$taskAll = @(Get-CimInstance Win32_Process)
$taskTracked = @(foreach ($taskExpectedRow in $taskExpected.Values) {
    $taskCurrent = @($taskAll | Where-Object ProcessId -eq $taskExpectedRow.ProcessId)
    $taskSame = $taskCurrent.Count -gt 0 -and $taskCurrent[0].CreationDate.ToUniversalTime().Ticks -eq ([datetime]$taskExpectedRow.creation_utc).ToUniversalTime().Ticks
    [pscustomobject]@{ pid=$taskExpectedRow.ProcessId; expected=$taskExpectedRow.creation_utc; same_process_live=$taskSame; reused_pid=$taskCurrent.Count -gt 0 -and -not $taskSame }
})
$taskMatches = @($taskAll | Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -like '*cursor-agent*' -and $_.CommandLine.Contains($taskProject) } | ForEach-Object {
    [pscustomobject]@{ pid=$_.ProcessId; name=$_.Name; creation_utc=$_.CreationDate.ToUniversalTime().ToString('o') }
})
$taskAGY = @($taskAll | Where-Object ProcessId -eq 44132 | ForEach-Object {
    [pscustomobject]@{ pid=$_.ProcessId; name=$_.Name; creation_utc=$_.CreationDate.ToUniversalTime().ToString('o'); expected_identity=$_.CreationDate.ToUniversalTime().Ticks -eq ([datetime]'2026-10-05T02:09:07.8897790Z').ToUniversalTime().Ticks }
})
$taskRecord = [ordered]@{ timestamp_utc=[datetime]::UtcNow.ToString('o'); stage=$Stage; project=$taskProject; port=$null; matching_count=$taskMatches.Count; matches=$taskMatches; tracked_live_count=@($taskTracked | Where-Object same_process_live).Count; tracked=$taskTracked; retained_agy_for_continuation=$taskAGY; process_stop_performed=$false; identity_source='union of start and before-stop captures' }
$taskTarget = Join-Path $taskRun $(if ($Stage -eq 'preflight') { 'process-preflight.json' } else { 'final-process-audit-attempt-02.json' })
if (Test-Path -LiteralPath $taskTarget) { throw 'Preserve existing audit' }
$taskRecord | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
[pscustomobject]@{ stage=$Stage; matching_count=$taskRecord.matching_count; tracked_live_count=$taskRecord.tracked_live_count; tracked_count=$taskTracked.Count; agy_retained=$taskAGY.Count } | ConvertTo-Json
if ($taskRecord.matching_count -ne 0 -or $taskRecord.tracked_live_count -ne 0) { throw 'Owned native process still live; reconcile before dependent work' }


