$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskTarget = Join-Path $taskRun 'final-process-audit-corrected.json'
if (Test-Path -LiteralPath $taskTarget) { throw 'Audit destination already exists' }
$taskOwner = Get-Content -LiteralPath (Join-Path $taskRun 'pipeline-process-ownership.json') -Raw | ConvertFrom-Json
$taskMonitor = Get-Content -LiteralPath (Join-Path $taskRun 'process-monitor-1708.json') -Raw | ConvertFrom-Json
$taskProcesses = @(Get-CimInstance Win32_Process)
function Test-TaskIdentity($actual, $expected) {
    if ($null -eq $actual) { return $false }
    return ([int]$actual.ProcessId -eq [int]$expected.ProcessId) -and
        ($actual.CreationDate.ToUniversalTime().Ticks -eq ([datetime]$expected.creation_utc).ToUniversalTime().Ticks)
}
$taskRoot = @($taskProcesses | Where-Object { $_.ProcessId -eq $taskOwner.root_pid })
$taskRootExpected = [pscustomobject]@{ ProcessId = $taskOwner.root_pid; creation_utc = $taskOwner.creation_utc }
$taskRootLive = $taskRoot.Count -eq 1 -and (Test-TaskIdentity $taskRoot[0] $taskRootExpected)
$taskTrackedLive = @(
    foreach ($expected in @($taskOwner.initial_tree) + @($taskMonitor.processes)) {
        foreach ($actual in $taskProcesses) {
            if (Test-TaskIdentity $actual $expected) {
                [pscustomobject]@{ ProcessId = $actual.ProcessId; ParentProcessId = $actual.ParentProcessId;
                    Name = $actual.Name; creation_utc = $actual.CreationDate.ToUniversalTime().ToString('o') }
            }
        }
    }
)
$taskTrackedLive = @($taskTrackedLive | Sort-Object ProcessId -Unique)
$taskMatches = @($taskProcesses | Where-Object {
    $_.ProcessId -ne $PID -and $_.Name -match '^python(?:w)?\.exe$' -and
    $_.CommandLine -and $_.CommandLine.IndexOf($taskRun, [StringComparison]::OrdinalIgnoreCase) -ge 0
} | ForEach-Object {
    [pscustomobject]@{ ProcessId = $_.ProcessId; ParentProcessId = $_.ParentProcessId; Name = $_.Name;
        creation_utc = $_.CreationDate.ToUniversalTime().ToString('o'); CommandLine = $_.CommandLine }
})
$taskAgy = @($taskProcesses | Where-Object {
    $_.ProcessId -eq 44132 -and $_.Name -eq 'Antigravity.exe' -and
    $_.CreationDate.ToUniversalTime().Ticks -eq ([datetime]'2026-10-05T02:09:07.8897790Z').ToUniversalTime().Ticks
} | ForEach-Object {
    [pscustomobject]@{ ProcessId = $_.ProcessId; Name = $_.Name; creation_utc = $_.CreationDate.ToUniversalTime().ToString('o') }
})
$taskStatus = if (!$taskRootLive -and $taskMatches.Count -eq 0 -and $taskTrackedLive.Count -eq 0) { 'pass' } else { 'live-owned-processes-observed' }
$taskAudit = [ordered]@{ timestamp_utc = [datetime]::UtcNow.ToString('o'); status = $taskStatus;
    root_pid = $taskOwner.root_pid; root_creation_utc = $taskOwner.creation_utc; root_still_live = $taskRootLive;
    matching_count = $taskMatches.Count; matching = $taskMatches; tracked_live_count = $taskTrackedLive.Count;
    tracked_live = $taskTrackedLive; auditor_pid_excluded = $PID; executable_filter = 'python.exe or pythonw.exe with exact owned run path';
    identity_check = 'PID and UTC creation ticks'; retained_agy = $taskAgy; port = $null; process_stop_performed = $false;
    original_audit = 'final-process-audit.json'; original_audit_sha256 = (Get-FileHash -LiteralPath (Join-Path $taskRun 'final-process-audit.json') -Algorithm SHA256).Hash.ToLowerInvariant();
    correction = 'Original filter matched audit shell PID 5144; original and failed verifier attempt retained' }
$taskAudit | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
$taskAudit | ConvertTo-Json -Depth 8
if ($taskStatus -ne 'pass') { exit 1 }
