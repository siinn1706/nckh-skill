$ErrorActionPreference = 'Stop'
$nckhAuditPath = Join-Path $PSScriptRoot 'final-process-audit.json'
if (Test-Path -LiteralPath $nckhAuditPath) { throw 'Preserve the existing final audit.' }
$nckhScopes = @('nckh-native-261005-0710-r35-attempt-01', 'nckh-native-261005-0658-r34-codex-file-attempt-01', 'nckh-native-261005-0052-r34-codex-attempt-01')
$nckhProcesses = @(Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -and $_.Name -match '^(python|codex|node|agent|agy)\.exe$'
})
$nckhMatches = @($nckhProcesses | Where-Object {
    $nckhCommand = $_.CommandLine
    @($nckhScopes | Where-Object { $nckhCommand.Contains($_) }).Count -gt 0
} | Select-Object ProcessId, ParentProcessId, CreationDate, Name, CommandLine)
$nckhResult = [PSCustomObject]@{
    status = $(if ($nckhMatches.Count -eq 0) { 'pass' } else { 'task-processes-remain' })
    recorded_at = [DateTimeOffset]::UtcNow.ToString('o')
    matching_task_processes = $nckhMatches
    scopes = $nckhScopes
    owner = '/root'
    ports_started = @()
    process_mutations = 'none; read-only observation after terminal owned sessions'
}
[System.IO.File]::WriteAllText($nckhAuditPath, ($nckhResult | ConvertTo-Json -Depth 8), [System.Text.UTF8Encoding]::new($false))
Write-Output ($nckhResult | Select-Object status, @{Name='matching_processes';Expression={$nckhMatches.Count}} | ConvertTo-Json -Compress)
if ($nckhMatches.Count -ne 0) { throw 'Inspect retained process evidence before finishing.' }
