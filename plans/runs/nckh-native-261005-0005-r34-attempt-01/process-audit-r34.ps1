$ErrorActionPreference = 'Stop'
$nckhAuditPath = Join-Path $PSScriptRoot 'final-process-audit.json'
if (Test-Path -LiteralPath $nckhAuditPath) { throw 'Preserve the existing process audit.' }
$nckhScopes = @(
    'nckh-native-261004-1707-attempt-01',
    'nckh-native-261004-2112-r31-attempt-01',
    'nckh-native-261004-2112-r32-attempt-01',
    'nckh-native-261004-2112-r33-attempt-01',
    'nckh-native-261005-0005-r34-attempt-01',
    'nckh-hooks-r34-0005-attempt-01'
)
$nckhProcesses = @(Get-CimInstance Win32_Process)
$nckhMatches = @($nckhProcesses | Where-Object {
    $nckhCandidate = $_
    $nckhCandidate.ProcessId -ne $PID -and
    $nckhCandidate.CommandLine -and
    $nckhCandidate.CommandLine -notlike '*process-audit-r34.ps1*' -and
    @($nckhScopes | Where-Object { $nckhCandidate.CommandLine.Contains($_) }).Count -gt 0
} | Select-Object ProcessId, ParentProcessId, CreationDate, Name, CommandLine)
$nckhResult = [PSCustomObject]@{
    recorded_at = [DateTimeOffset]::UtcNow.ToString('o')
    owner = '/root'
    work_context = 'C:/Users/USER\Downloads\test-skill'
    source_revision = 34
    source_lock_hash = '8ca3304f3c906b0a3421c38fbb32c939ec23839537e9b9c5fc23421da0a21b34'
    scope = $nckhScopes
    matching_task_processes = $nckhMatches
    ports_started = @()
    process_mutations = 'none; read-only ownership reconciliation'
    status = $(if ($nckhMatches.Count -eq 0) { 'pass' } else { 'owned-processes-remain' })
}
[System.IO.File]::WriteAllText($nckhAuditPath, ($nckhResult | ConvertTo-Json -Depth 8), [System.Text.UTF8Encoding]::new($false))
Write-Output ($nckhResult | Select-Object status, @{Name='matching_processes';Expression={$nckhMatches.Count}} | ConvertTo-Json -Compress)
if ($nckhMatches.Count -ne 0) { throw 'Inspect retained ownership evidence before finalization.' }
