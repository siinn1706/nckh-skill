$ErrorActionPreference='Stop'
$taskRun=$PSScriptRoot
$taskPrepared=Get-Content -LiteralPath (Join-Path $taskRun 'preparation.json') -Raw | ConvertFrom-Json
$taskAll=@(Get-CimInstance Win32_Process)
$taskCandidates=@($taskAll | Where-Object {$_.Name -eq 'node.exe' -and $_.CommandLine -like '*cursor-agent*' -and $_.CommandLine.Contains($taskPrepared.project)})
$taskRoots=@($taskCandidates | Where-Object {$taskCandidates.ProcessId -notcontains $_.ParentProcessId})
if($taskRoots.Count -ne 1){throw ('Expected one owned Cursor root; found '+$taskRoots.Count)}
$taskRoot=$taskRoots[0]
$taskRecord=[ordered]@{pid=$taskRoot.ProcessId;parent_pid=$taskRoot.ParentProcessId;name=$taskRoot.Name;creation_utc=$taskRoot.CreationDate.ToUniversalTime().ToString('o');creation_cim_ticks=$taskRoot.CreationDate.ToUniversalTime().ToFileTimeUtc();project=$taskPrepared.project}
$taskTarget=Join-Path $taskRun 'native-root-selection.json'
if(Test-Path -LiteralPath $taskTarget){throw 'Preserve prior root selection'}
$taskRecord | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $taskTarget -Encoding utf8NoBOM
$taskRecord | ConvertTo-Json
