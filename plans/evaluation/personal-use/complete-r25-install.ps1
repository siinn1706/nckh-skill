$ErrorActionPreference = 'Stop'
$taskProject = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$taskExpectedProject = 'C:/Users/USER\Downloads\test-skill'
if (-not [StringComparer]::OrdinalIgnoreCase.Equals($taskProject, $taskExpectedProject)) {
    throw 'This handoff is restricted to the approved test-skill project.'
}
$taskPython = 'C:/Users/USER\AppData\Local\Programs\Python\Python312\python.exe'
if (-not (Test-Path -LiteralPath $taskPython -PathType Leaf)) {
    throw 'The verified Python runtime is unavailable.'
}
$taskPackage = Join-Path $taskProject 'plans/evaluation/personal-use/candidate-r25-attempt-02/bundles/on/codex'
$taskEvidence = Join-Path $taskProject 'plans/evaluation/personal-use/candidate-r25-attempt-02/candidate-evidence.json'
$taskInstaller = Join-Path $PSScriptRoot 'install-candidate.py'
$taskRun = Join-Path $PSScriptRoot ('install-r25-manual-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fffffff'))
[void](New-Item -ItemType Directory -Path $taskRun)
$taskUtf8 = [Text.UTF8Encoding]::new($false)
$taskReceipt = [ordered]@{
    project = $taskProject
    route = 'user-foreground-powershell'
    powershell_pid = $PID
    started_at = [DateTime]::UtcNow.ToString('o')
    status = 'running'
    stage = 'preview'
    candidate_revision = '25'
    source_lock_hash = 'adc6422394da5a833e1059d922b27c5658eb6699b2ab950568a557d48d71968c'
    install_id = 'd5811d724fe29cb5016c7c3a'
    output = $taskRun
}
function Save-TaskReceipt {
    [IO.File]::WriteAllText((Join-Path $taskRun 'receipt.json'), (($taskReceipt | ConvertTo-Json -Depth 10) + "`n"), $taskUtf8)
}
function Invoke-TaskUpdate([string]$Folder, [switch]$Commit) {
    $taskArguments = @('-B', $taskInstaller, '--package', $taskPackage, '--evidence', $taskEvidence, '--output', $Folder)
    if ($Commit) { $taskArguments += '--commit' }
    & $taskPython @taskArguments
    if ($LASTEXITCODE -ne 0) { throw "Installer failed; retained receipts: $Folder" }
    Get-Content -Raw -LiteralPath (Join-Path $Folder 'stdout.json') | ConvertFrom-Json
}
function Read-TaskPreview([string]$Folder) {
    Get-Content -Raw -LiteralPath (Join-Path $Folder 'stdout.json') | ConvertFrom-Json
}
Save-TaskReceipt
try {
    $taskPreviewFolder = Join-Path $taskRun 'preview'
    Invoke-TaskUpdate $taskPreviewFolder | Out-Host
    $taskPreview = Read-TaskPreview $taskPreviewFolder
    $taskChanges = @($taskPreview.transaction.entries | Where-Object action -ne 'unchanged')
    if ($taskPreview.status -ne 'preview' -or $taskPreview.transaction.install_id -ne $taskReceipt.install_id -or
        @($taskPreview.transaction.conflicts).Count -ne 0 -or @($taskPreview.transaction.entries).Count -ne 43 -or
        $taskChanges.Count -ne 1 -or $taskChanges[0].action -ne 'replace' -or $taskChanges[0].skill -ne 'nckh-visuals' -or
        $taskChanges[0].before_hash -ne '926c745ec2c504abf67aeccd9b0591bf82f57422f90fbd47f6c24b4e59b0b43f' -or
        $taskChanges[0].tree_hash -ne 'fe0403204d22a2aa5e5b1dc587bd959cbb340d7784109e359c8de3eccc5116e0') {
        throw 'The fresh preview differs from the reviewed one-item r25 update. Keep the receipts for review.'
    }
    $taskReceipt.stage = 'update'; Save-TaskReceipt
    Invoke-TaskUpdate (Join-Path $taskRun 'update') -Commit | Out-Host

    $taskReceipt.stage = 'doctor'; Save-TaskReceipt
    $taskDoctorArguments = @('-B', (Join-Path $taskProject 'nckh-kit/installer/nckh-installer.py'), 'doctor', '--state-dir', (Join-Path $taskProject '.nckh-state'))
    $taskDoctorText = & $taskPython @taskDoctorArguments 2> (Join-Path $taskRun 'doctor.stderr.txt')
    if ($LASTEXITCODE -ne 0) { throw 'Post-install doctor failed; inspect its retained output.' }
    [IO.File]::WriteAllText((Join-Path $taskRun 'doctor.json'), (($taskDoctorText -join "`n") + "`n"), $taskUtf8)
    $taskDoctor = ($taskDoctorText -join "`n") | ConvertFrom-Json
    if (@($taskDoctor.items).Count -ne 43 -or @($taskDoctor.items | Where-Object status -ne 'current').Count -ne 0) {
        throw 'Post-install doctor does not show all 43 owned items current.'
    }

    $taskReceipt.stage = 'post-preview'; Save-TaskReceipt
    $taskPostFolder = Join-Path $taskRun 'post-preview'
    Invoke-TaskUpdate $taskPostFolder | Out-Host
    $taskPost = Read-TaskPreview $taskPostFolder
    if ($taskPost.status -ne 'preview' -or @($taskPost.transaction.conflicts).Count -ne 0 -or
        @($taskPost.transaction.entries).Count -ne 43 -or @($taskPost.transaction.entries | Where-Object action -ne 'unchanged').Count -ne 0) {
        throw 'Post-install preview is not an unchanged 43-item transaction.'
    }

    $taskReceipt.stage = 'installed-bindings'; Save-TaskReceipt
    $taskChecker = Join-Path $taskProject '.agents/skills/nckh-visuals/references/_shared/scripts/check-visual-engine.py'
    foreach ($taskHost in @('cursor', 'agy', 'codex')) {
        $taskBinding = 'plans/evaluation/personal-use/visual-engine-probe-02/' + $taskHost + '-binding.json'
        $taskBindingArguments = @('-I', $taskChecker, '--project', $taskProject, '--task', 'real-source-worldbank-visual-01', '--host', $taskHost, '--binding', $taskBinding, '--capability', 'svg-render')
        $taskBindingText = & $taskPython @taskBindingArguments 2> (Join-Path $taskRun ('binding-' + $taskHost + '.stderr.txt'))
        [IO.File]::WriteAllText((Join-Path $taskRun ('binding-' + $taskHost + '.json')), (($taskBindingText -join "`n") + "`n"), $taskUtf8)
        if ($LASTEXITCODE -ne 0 -or (($taskBindingText -join "`n") | ConvertFrom-Json).status -ne 'integrity-verified') {
            throw "The installed binding check failed for $taskHost."
        }
    }
    $taskReceipt.status = 'completed-checks-passed'
    $taskReceipt.stage = 'complete'
    $taskReceipt.finished_at = [DateTime]::UtcNow.ToString('o')
    Save-TaskReceipt
    Write-Output "r25 installation checks passed. Receipts: $taskRun"
} catch {
    $taskReceipt.status = 'failed'
    $taskReceipt.error = $_.Exception.Message
    $taskReceipt.finished_at = [DateTime]::UtcNow.ToString('o')
    Save-TaskReceipt
    throw
}
