$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskPrepared = Get-Content -LiteralPath (Join-Path $taskRun 'preparation.json') -Raw | ConvertFrom-Json
$taskProcesses = @(Get-CimInstance Win32_Process)
$taskMatches = @($taskProcesses | Where-Object { $_.Name -match '^(?:node|python(?:w)?)\.exe$' -and $_.CommandLine -and (($_.Name -eq 'node.exe' -and $_.CommandLine -like '*cursor-agent*' -and $_.CommandLine.Contains($taskPrepared.project)) -or $_.CommandLine.Contains($taskRun)) } | ForEach-Object { [pscustomobject]@{pid=$_.ProcessId; parent_pid=$_.ParentProcessId; name=$_.Name; creation_utc=$_.CreationDate.ToUniversalTime().ToString('o')} })
$taskMcp = @($taskProcesses | Where-Object { $_.Name -match '^(?:node|cmd)\.exe$' -and $_.CommandLine -and $_.CommandLine -like '*illustrator-mcp-server*' } | ForEach-Object { [pscustomobject]@{pid=$_.ProcessId; parent_pid=$_.ParentProcessId; name=$_.Name; creation_utc=$_.CreationDate.ToUniversalTime().ToString('o')} })
$taskTarget = Join-Path $taskRun 'final-process-audit.json'
if (Test-Path -LiteralPath $taskTarget) { throw 'Preserve final admission audit' }
$taskRecord = [ordered]@{timestamp_utc=[datetime]::UtcNow.ToString('o'); matching_count=$taskMatches.Count; matches=$taskMatches; tracked_live_count=0; tracked=@(); ownership_capture='native root exited before capture; no PID invented'; illustrator_startup_process_count=$taskMcp.Count; illustrator_startup_processes=$taskMcp; process_stop_performed=$false; retained_agy_for_continuation=@($taskProcesses | Where-Object ProcessId -eq 44132 | Select-Object ProcessId,Name,@{Name='creation_utc';Expression={$_.CreationDate.ToUniversalTime().ToString('o')}})}
$taskRecord | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
[pscustomobject]@{matching_count=$taskMatches.Count; illustrator_startup_process_count=$taskMcp.Count; ownership_capture=$taskRecord.ownership_capture} | ConvertTo-Json
if ($taskMatches.Count -ne 0) { exit 1 }
