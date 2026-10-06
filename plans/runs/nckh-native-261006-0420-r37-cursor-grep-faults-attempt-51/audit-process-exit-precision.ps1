param()
$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskOriginal = Get-Content -LiteralPath (Join-Path $taskRun 'process-final-audit.json') -Raw | ConvertFrom-Json
$taskAll = @(Get-CimInstance Win32_Process)
$taskByPid = @{}
foreach ($taskProcess in $taskAll) { $taskByPid[[int]$taskProcess.ProcessId] = $taskProcess }
$taskRows = @(foreach ($taskIdentity in $taskOriginal.tracked) {
    $taskCurrent = $taskByPid[[int]$taskIdentity.pid]
    $taskCurrentTicks = if ($null -ne $taskCurrent) { $taskCurrent.CreationDate.ToUniversalTime().ToFileTimeUtc() } else { $null }
    $taskSame = $null -ne $taskCurrentTicks -and [math]::Abs([decimal]$taskCurrentTicks - [decimal]$taskIdentity.creation_filetime_ticks) -le 9
    [pscustomobject]@{ pid=$taskIdentity.pid; recorded_ticks=$taskIdentity.creation_filetime_ticks; current_cim_ticks=$taskCurrentTicks; matches_within_cim_microsecond_precision=$taskSame; current_pid_present=$null -ne $taskCurrent }
})
$taskRecord = [ordered]@{
    timestamp_utc=[datetime]::UtcNow.ToString('o')
    status='supplemental-read-only-CIM-precision-exit-audit'
    original_audit_sha256=(Get-FileHash -LiteralPath (Join-Path $taskRun 'process-final-audit.json') -Algorithm SHA256).Hash.ToLowerInvariant()
    identity_count=$taskRows.Count
    matching_identity_count=@($taskRows | Where-Object matches_within_cim_microsecond_precision).Count
    comparison='same PID and creation timestamps within 9 FILETIME ticks, accounting for CIM microsecond precision'
    monitor_failure_preserved=$true
    continuous_monitor_success=$false
    process_stop_performed=$false
    identities=$taskRows
}
$taskTarget=Join-Path $taskRun 'process-exit-precision-audit.json'
if (Test-Path -LiteralPath $taskTarget) { throw 'Preserve prior precision audit' }
$taskRecord | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
[pscustomobject]@{status=$taskRecord.status;identities=$taskRows.Count;matching_live=$taskRecord.matching_identity_count} | ConvertTo-Json
if ($taskRecord.matching_identity_count -ne 0) { throw 'An owned process may remain live' }
