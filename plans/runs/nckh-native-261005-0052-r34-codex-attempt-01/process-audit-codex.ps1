$ErrorActionPreference = 'Stop'
$nckhAuditPath = Join-Path $PSScriptRoot 'post-cleanup-process-audit.json'
if (Test-Path -LiteralPath $nckhAuditPath) { throw 'Preserve the existing audit.' }
$nckhScope = 'nckh-native-261005-0052-r34-codex-attempt-01'
$nckhMatches = @(Get-CimInstance Win32_Process | Where-Object {
    $_.ProcessId -ne $PID -and $_.CommandLine -and $_.CommandLine.Contains($nckhScope) -and
    $_.CommandLine -notlike '*process-audit-codex.ps1*'
} | Select-Object ProcessId, ParentProcessId, CreationDate, Name, CommandLine)
$nckhResult = [PSCustomObject]@{
    status = $(if ($nckhMatches.Count -eq 0) { 'pass' } else { 'task-processes-remain' })
    recorded_at = [DateTimeOffset]::UtcNow.ToString('o')
    matching_task_processes = $nckhMatches
    work_context = 'C:/Users/USER\Downloads\test-skill'
    owner = '/root'
    ports_started = @()
    process_mutations = 'none; read-only reconciliation'
}
[System.IO.File]::WriteAllText($nckhAuditPath, ($nckhResult | ConvertTo-Json -Depth 8), [System.Text.UTF8Encoding]::new($false))
Write-Output ($nckhResult | Select-Object status, @{Name='matching_processes';Expression={$nckhMatches.Count}} | ConvertTo-Json -Compress)
if ($nckhMatches.Count -ne 0) { throw 'Inspect retained process evidence.' }
