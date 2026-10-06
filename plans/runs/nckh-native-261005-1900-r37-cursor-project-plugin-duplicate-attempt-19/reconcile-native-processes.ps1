param([Parameter(Mandatory=$true)][ValidateSet('graceful','force','audit')][string]$Stage)

$nativeRunDir = $PSScriptRoot
$nativeOwnedTree = Get-Content -LiteralPath (Join-Path $nativeRunDir 'process-tree-before-stop.json') -Raw | ConvertFrom-Json
$nativeOwnership = Get-Content -LiteralPath (Join-Path $nativeRunDir 'native-process-ownership.json') -Raw | ConvertFrom-Json
$nativeAllRows = @(Get-CimInstance Win32_Process)
$nativeIdentityChecks = foreach ($nativeExpectedRow in $nativeOwnedTree.processes) {
    $nativeCurrentRows = @($nativeAllRows | Where-Object ProcessId -eq $nativeExpectedRow.ProcessId)
    if ($nativeCurrentRows.Count -and $nativeCurrentRows[0].CreationDate.ToUniversalTime().Ticks -ne ([DateTime]$nativeExpectedRow.creation_utc).ToUniversalTime().Ticks) {
        throw ('Owned process creation identity changed: ' + $nativeExpectedRow.ProcessId)
    }
    [pscustomobject]@{
        pid=$nativeExpectedRow.ProcessId
        expected=$nativeExpectedRow.creation_utc
        current=if($nativeCurrentRows.Count){$nativeCurrentRows[0].CreationDate.ToUniversalTime().ToString('o')}else{$null}
    }
}

if ($Stage -eq 'audit') {
    $nativeMatches = @($nativeAllRows | Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -like '*cursor-agent*' -and $_.CommandLine.Contains($nativeOwnership.project) } | Select-Object ProcessId,ParentProcessId,Name,@{Name='creation_utc';Expression={$_.CreationDate.ToUniversalTime().ToString('o')}})
    $nativeRecord = [pscustomobject]@{
        timestamp_utc=[DateTime]::UtcNow.ToString('o')
        matching_count=$nativeMatches.Count
        matches=$nativeMatches
        tracked_live_count=@($nativeIdentityChecks | Where-Object current -ne $null).Count
        tracked=$nativeIdentityChecks
        retained_agy_for_continuation=@($nativeAllRows | Where-Object ProcessId -eq 44132 | Select-Object ProcessId,Name,@{Name='creation_utc';Expression={$_.CreationDate.ToUniversalTime().ToString('o')}})
    }
    $nativeReceiptPath = Join-Path $nativeRunDir 'final-process-audit.json'
} else {
    $nativeRootRow = @($nativeAllRows | Where-Object ProcessId -eq $nativeOwnedTree.root_pid)
    if ($nativeRootRow.Count -ne 1 -or $nativeRootRow[0].Name -ne 'node.exe' -or $nativeRootRow[0].CommandLine -notlike '*cursor-agent*' -or -not $nativeRootRow[0].CommandLine.Contains($nativeOwnership.project)) {
        throw 'Owned Cursor root absent or no longer matches its project; reconcile survivors separately'
    }
    if ($Stage -eq 'force') {
        $nativeGraceful = Get-Content -LiteralPath (Join-Path $nativeRunDir 'process-stop-graceful.json') -Raw | ConvertFrom-Json
        if ($nativeGraceful.exit_code -eq 0) { throw 'Force stop not needed after successful graceful stop' }
        $nativeStopOutput = @(& taskkill.exe /PID $nativeOwnedTree.root_pid /T /F 2>&1 | ForEach-Object { $_.ToString() })
    } else {
        $nativeStopOutput = @(& taskkill.exe /PID $nativeOwnedTree.root_pid /T 2>&1 | ForEach-Object { $_.ToString() })
    }
    $nativeStopCode = $LASTEXITCODE
    $nativeRecord = [pscustomobject]@{
        root_pid=$nativeOwnedTree.root_pid
        comparison='exact-UTC-ticks'
        timestamp_utc=[DateTime]::UtcNow.ToString('o')
        identity_checks=$nativeIdentityChecks
        method=if($Stage -eq 'force'){'force-owned-tree-after-graceful-refusal'}else{'graceful-owned-tree-after-native-exit-request'}
        exit_code=$nativeStopCode
        output=$nativeStopOutput
    }
    $nativeReceiptPath = Join-Path $nativeRunDir ('process-stop-' + $Stage + '.json')
}

if (Test-Path -LiteralPath $nativeReceiptPath) { throw ('Preserve existing receipt: ' + $nativeReceiptPath) }
$nativeRecord | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $nativeReceiptPath -Encoding utf8
if ($Stage -eq 'audit') {
    [pscustomobject]@{stage=$Stage;matching_count=$nativeRecord.matching_count;tracked_live_count=$nativeRecord.tracked_live_count} | ConvertTo-Json
} else {
    [pscustomobject]@{stage=$Stage;root_pid=$nativeRecord.root_pid;exit_code=$nativeRecord.exit_code;identity_checks=@($nativeRecord.identity_checks).Count} | ConvertTo-Json
}
