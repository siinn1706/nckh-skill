$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskWork = Split-Path (Split-Path (Split-Path $taskRun -Parent) -Parent) -Parent
$taskAudit = Get-Content -LiteralPath (Join-Path $taskRun 'process-exit-precision-audit.json') -Raw | ConvertFrom-Json
$taskSelected = @($taskAudit.identities | Where-Object matches_within_cim_microsecond_precision)
$taskAll = @(Get-CimInstance Win32_Process)
$taskRecords = @(foreach ($taskIdentity in $taskSelected) {
    $taskCurrent = @($taskAll | Where-Object ProcessId -eq $taskIdentity.pid)
    if ($taskCurrent.Count -ne 1) { continue }
    $taskProcess = $taskCurrent[0]
    $taskTicks = $taskProcess.CreationDate.ToUniversalTime().ToFileTimeUtc()
    $taskCommand = [string]$taskProcess.CommandLine
    $taskHasher = [System.Security.Cryptography.SHA256]::Create()
    $taskBytes = [System.Text.Encoding]::UTF8.GetBytes($taskCommand)
    $taskHash = [Convert]::ToHexString($taskHasher.ComputeHash($taskBytes)).ToLowerInvariant()
    $taskHasher.Dispose()
    $taskTokens = [regex]::Matches($taskCommand,'[^\s"]*(?:cursor-agent|nckh-native-[^\s"\\/]*|Antigravity|agy)[^\s"]*') | ForEach-Object {$_.Value}
    [pscustomobject]@{
        pid=$taskProcess.ProcessId
        parent_pid=$taskProcess.ParentProcessId
        name=$taskProcess.Name
        creation_utc=$taskProcess.CreationDate.ToUniversalTime().ToString('o')
        creation_filetime_ticks=$taskTicks
        matches_retained_precision=[math]::Abs([decimal]$taskTicks - [decimal]$taskIdentity.recorded_ticks) -le 9
        executable_path=$taskProcess.ExecutablePath
        command_sha256=$taskHash
        command_contains_work=$taskCommand.Contains($taskWork)
        command_contains_current_run=$taskCommand.Contains($taskRun)
        bounded_relevant_path_tokens=@($taskTokens | Select-Object -First 5)
    }
})
$taskPath=Join-Path $taskRun 'live-process-identity-inspection.json'
if (Test-Path -LiteralPath $taskPath) {throw 'Preserve previous inspection'}
[ordered]@{timestamp_utc=[datetime]::UtcNow.ToString('o');source_audit='process-exit-precision-audit.json';rows=$taskRecords;process_stop_performed=$false;raw_commandline_stored=$false} | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $taskPath -Encoding utf8NoBOM
$taskRecords | ConvertTo-Json -Depth 5
