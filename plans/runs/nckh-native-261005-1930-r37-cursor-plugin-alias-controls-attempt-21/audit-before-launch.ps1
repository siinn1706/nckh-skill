$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskWork = (Resolve-Path -LiteralPath (Join-Path $taskRun '..\..\..')).Path
$taskProject = Join-Path $taskWork 'plans\runs\nckh-native-261005-0128-r34-cursor-events-attempt-02\projects\main'
$taskTarget = Join-Path $taskRun 'prelaunch-process-audit.json'
if (Test-Path -LiteralPath $taskTarget) { throw 'Preserve existing preflight receipt' }
$taskProcesses = @(Get-CimInstance Win32_Process)
$taskEarlierRuns = @(
    'nckh-native-261005-1740-r37-cursor-private-mutation-attempt-16',
    'nckh-native-261005-1755-r37-cursor-preflight-faults-attempt-17',
    'nckh-native-261005-1842-r37-cursor-private-create-attempt-18',
    'nckh-native-261005-1900-r37-cursor-project-plugin-duplicate-attempt-19',
    'nckh-native-261005-1640-r37-cursor-timeout-repair-attempt-02'
)
$taskTracked = @()
foreach ($taskEarlier in $taskEarlierRuns[0..3]) {
    $taskAudit = Get-Content -LiteralPath (Join-Path $taskWork ('plans\runs\' + $taskEarlier + '\final-process-audit.json')) -Raw | ConvertFrom-Json
    foreach ($taskExpected in $taskAudit.tracked) {
        $taskActual = @($taskProcesses | Where-Object ProcessId -eq $taskExpected.pid)
        $taskIdentity = $taskActual.Count -eq 1 -and $taskActual[0].CreationDate.ToUniversalTime().Ticks -eq ([datetime]$taskExpected.expected).ToUniversalTime().Ticks
        $taskTracked += [pscustomobject]@{ pid=$taskExpected.pid; expected=$taskExpected.expected; same_process_live=$taskIdentity }
    }
}
$taskMatches = @($taskProcesses | Where-Object {
    if ($_.ProcessId -eq $PID -or !$_.CommandLine -or $_.Name -notmatch '^(?:python(?:w)?|node)\.exe$') { return $false }
    if ($_.Name -eq 'node.exe' -and $_.CommandLine -like '*cursor-agent*' -and $_.CommandLine.Contains($taskProject)) { return $true }
    foreach ($taskEarlier in $taskEarlierRuns + @(Split-Path -Leaf $taskRun)) {
        if ($_.CommandLine.Contains((Join-Path $taskWork ('plans\runs\' + $taskEarlier)))) { return $true }
    }
    return $false
} | ForEach-Object {
    [pscustomobject]@{ pid=$_.ProcessId; parent_pid=$_.ParentProcessId; name=$_.Name; creation_utc=$_.CreationDate.ToUniversalTime().ToString('o') }
})
$taskAgy = @($taskProcesses | Where-Object {
    $_.ProcessId -eq 44132 -and $_.Name -eq 'Antigravity.exe' -and $_.CreationDate.ToUniversalTime().Ticks -eq ([datetime]'2026-10-05T02:09:07.8897790Z').ToUniversalTime().Ticks
} | ForEach-Object { [pscustomobject]@{ pid=$_.ProcessId; name=$_.Name; creation_utc=$_.CreationDate.ToUniversalTime().ToString('o') } })
$taskReceipt = [ordered]@{ timestamp_utc=[datetime]::UtcNow.ToString('o'); matching_count=$taskMatches.Count; matches=$taskMatches;
    tracked_live_count=@($taskTracked | Where-Object same_process_live).Count; tracked=$taskTracked; retained_agy=$taskAgy;
    process_stop_performed=$false; identity_check='PID plus UTC creation ticks'; project=$taskProject; port=$null }
$taskReceipt | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
$taskReceipt | ConvertTo-Json -Depth 7
if ($taskReceipt.matching_count -ne 0 -or $taskReceipt.tracked_live_count -ne 0) { exit 1 }
