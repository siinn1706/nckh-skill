param([Parameter(Mandatory=$true)][ValidateSet('start','before-stop','progress')][string]$Stage)
$ErrorActionPreference = 'Stop'
$taskRun = $PSScriptRoot
$taskPrepared = Get-Content -LiteralPath (Join-Path $taskRun 'preparation.json') -Raw | ConvertFrom-Json
$taskProcesses = @(Get-CimInstance Win32_Process)
if ($Stage -eq 'start') {
    $taskCandidates = @($taskProcesses | Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -like '*cursor-agent*' -and $_.CommandLine.Contains($taskPrepared.project) })
    $taskRoots = @($taskCandidates | Where-Object { $taskCandidates.ProcessId -notcontains $_.ParentProcessId })
    if ($taskRoots.Count -ne 1) { throw ('Expected one Cursor root, found ' + $taskRoots.Count) }
    $taskRootPid = [int]$taskRoots[0].ProcessId
} else {
    $taskOwned = Get-Content -LiteralPath (Join-Path $taskRun 'native-process-ownership.json') -Raw | ConvertFrom-Json
    $taskRootPid = [int]$taskOwned.root_pid
    $taskRoots = @($taskProcesses | Where-Object ProcessId -eq $taskRootPid)
    if ($taskRoots.Count -ne 1 -or $taskRoots[0].CreationDate.ToUniversalTime().Ticks -ne ([datetime]$taskOwned.creation_utc).ToUniversalTime().Ticks) { throw 'Cursor root identity no longer live' }
}
$taskIds = [System.Collections.Generic.HashSet[int]]::new()
[void]$taskIds.Add($taskRootPid)
do {
    $taskAdded = $false
    foreach ($taskRow in $taskProcesses) {
        if ($taskIds.Contains([int]$taskRow.ParentProcessId) -and $taskIds.Add([int]$taskRow.ProcessId)) { $taskAdded = $true }
    }
} while ($taskAdded)
$taskRows = @($taskProcesses | Where-Object { $taskIds.Contains([int]$_.ProcessId) } | ForEach-Object {
    [pscustomobject]@{ ProcessId=$_.ProcessId; ParentProcessId=$_.ParentProcessId; Name=$_.Name; creation_utc=$_.CreationDate.ToUniversalTime().ToString('o') }
})
$taskTree = [ordered]@{ root_pid=$taskRootPid; creation_utc=$taskRoots[0].CreationDate.ToUniversalTime().ToString('o'); timestamp_utc=[datetime]::UtcNow.ToString('o'); processes=$taskRows; port=$null }
$taskTarget = Join-Path $taskRun ('process-tree-' + $Stage + '.json')
if (Test-Path -LiteralPath $taskTarget) { throw 'Preserve existing process capture' }
$taskTree | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
if ($Stage -eq 'start') {
    $taskTerminal = Get-Content -LiteralPath (Join-Path $taskRun 'terminal-start.json') -Raw | ConvertFrom-Json
    $taskOwnership = [ordered]@{ root_pid=$taskRootPid; creation_utc=$taskTree.creation_utc; session_id=$taskTerminal.session_id; project=$taskPrepared.project;
        command='Cursor interactive: --force --trust --sandbox disabled --workspace owned project; granted model through existing selectedModel'; model=$taskPrepared.model; port=$null; worktree=$taskPrepared.project; owner='/root' }
    $taskOwnership | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $taskRun 'native-process-ownership.json') -Encoding utf8NoBOM
}
[pscustomobject]@{ stage=$Stage; root_pid=$taskRootPid; processes=$taskRows.Count; creation_utc=$taskTree.creation_utc } | ConvertTo-Json
