$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskWork = (Resolve-Path -LiteralPath (Join-Path $taskRun '..\..\..')).Path
$taskRuns = @('nckh-native-261005-1930-r37-cursor-plugin-alias-controls-attempt-21','nckh-native-261005-2119-r37-cursor-selected-model-search-attempt-24')
$taskProcesses = @(Get-CimInstance Win32_Process)
$taskRecords = @(foreach ($taskName in $taskRuns) {
    $taskDirectory = Join-Path $taskWork ('plans\runs\' + $taskName)
    $taskOwner = Get-Content -LiteralPath (Join-Path $taskDirectory 'native-process-ownership.json') -Raw | ConvertFrom-Json
    if ($taskOwner.owner -ne '/root') { throw 'Task controller ownership missing' }
    $taskUnique = @{}
    foreach ($taskStage in @('start','before-stop')) {
        $taskCapture = Get-Content -LiteralPath (Join-Path $taskDirectory ('process-tree-' + $taskStage + '.json')) -Raw | ConvertFrom-Json
        foreach ($taskExpected in $taskCapture.processes) {
            $taskKey = '{0}|{1}' -f $taskExpected.ProcessId,([datetime]$taskExpected.creation_utc).ToUniversalTime().Ticks
            $taskUnique[$taskKey] = $taskExpected
        }
    }
    $taskIdentities = @(foreach ($taskExpected in $taskUnique.Values) {
        $taskActual = @($taskProcesses | Where-Object ProcessId -eq $taskExpected.ProcessId)
        $taskSame = $taskActual.Count -eq 1 -and $taskActual[0].CreationDate.ToUniversalTime().Ticks -eq ([datetime]$taskExpected.creation_utc).ToUniversalTime().Ticks
        [pscustomobject]@{pid=$taskExpected.ProcessId; expected=$taskExpected.creation_utc; same_process_live=$taskSame; current_creation_utc=if($taskActual.Count){$taskActual[0].CreationDate.ToUniversalTime().ToString('o')}else{$null}}
    })
    $taskMatches = @($taskProcesses | Where-Object { $_.Name -match '^(?:node|python(?:w)?)\.exe$' -and $_.CommandLine -and (( $_.Name -eq 'node.exe' -and $_.CommandLine -like '*cursor-agent*' -and $_.CommandLine.Contains($taskOwner.project)) -or $_.CommandLine.Contains($taskDirectory)) } | Select-Object ProcessId,Name)
    [pscustomobject]@{run=$taskName; project=$taskOwner.project; root_pid=$taskOwner.root_pid; observed_identity_count=$taskIdentities.Count; tracked_live_count=@($taskIdentities | Where-Object same_process_live).Count; matching_count=$taskMatches.Count; matches=$taskMatches; tracked=$taskIdentities}
})
$taskTarget = Join-Path $taskRun 'all-observed-process-audit.json'
if (Test-Path -LiteralPath $taskTarget) { throw 'Preserve union audit receipt' }
$taskRecord = [ordered]@{timestamp_utc=[datetime]::UtcNow.ToString('o'); status='audited-start-and-before-stop-identity-union'; runs=$taskRecords; process_stop_performed=$false; retained_agy=@($taskProcesses | Where-Object { $_.ProcessId -eq 44132 -and $_.CreationDate.ToUniversalTime().Ticks -eq ([datetime]'2026-10-05T02:09:07.8897790Z').ToUniversalTime().Ticks } | Select-Object ProcessId,Name)}
$taskRecord | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
$taskRecords | Select-Object run,observed_identity_count,tracked_live_count,matching_count | ConvertTo-Json
if (@($taskRecords | Where-Object { $_.tracked_live_count -ne 0 -or $_.matching_count -ne 0 }).Count -ne 0) { exit 1 }
