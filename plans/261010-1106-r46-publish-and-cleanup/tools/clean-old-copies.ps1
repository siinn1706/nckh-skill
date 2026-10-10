param(
    [switch]$Apply,
    [ValidateSet('generated-packages', 'rollback-payloads')]
    [string]$Scope = 'generated-packages'
)

$ErrorActionPreference = 'Stop'
$nckhRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$nckhRootPrefix = $nckhRoot.TrimEnd('\') + '\'
$nckhReleaseState = Join-Path $nckhRoot '.nckh-state/release-r46-261010'
$nckhVerified = Get-Content -LiteralPath (Join-Path $nckhReleaseState 'installed-verification.json') -Raw | ConvertFrom-Json
if ($nckhVerified.status -ne 'pass' -or $nckhVerified.global_items -ne 239 -or $nckhVerified.project_items -ne 49) {
    throw 'Verified replacement of every owned destination is required before cleanup.'
}

$nckhTargets = [Collections.Generic.List[string]]::new()
if ($Scope -eq 'generated-packages') {
    foreach ($nckhRelative in @('nckh-kit/dist-before-update-2026-10-06', '.nckh-state/release-r46-261010/previous-packages')) {
        $nckhCandidate = Join-Path $nckhRoot $nckhRelative
        if (Test-Path -LiteralPath $nckhCandidate) { $nckhTargets.Add($nckhCandidate) }
    }
}
if ($Scope -eq 'rollback-payloads') {
Get-ChildItem -LiteralPath (Join-Path $nckhRoot '.nckh-state/global-deployment-runs') -Directory -Force |
    Where-Object Name -Like 'global-backups-*' | ForEach-Object { $nckhTargets.Add($_.FullName) }
foreach ($nckhTransaction in (Get-ChildItem -LiteralPath (Join-Path $nckhRoot '.nckh-state/transactions') -Directory -Force)) {
    if ($nckhTransaction.Name -notmatch '^[a-f0-9]{32}$') { continue }
    Get-ChildItem -LiteralPath $nckhTransaction.FullName -Force |
        Where-Object Name -Match '^(backup|stage)-[0-9]+$' | ForEach-Object { $nckhTargets.Add($_.FullName) }
}
}

$nckhInventory = @()
foreach ($nckhTarget in $nckhTargets) {
    $nckhResolved = (Resolve-Path -LiteralPath $nckhTarget).ProviderPath
    if (-not $nckhResolved.StartsWith($nckhRootPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Cleanup target escapes the workspace: $nckhResolved"
    }
    $nckhItem = Get-Item -LiteralPath $nckhResolved -Force
    $nckhMembers = if ($nckhItem.PSIsContainer) { @(Get-ChildItem -LiteralPath $nckhResolved -Recurse -Force) } else { @($nckhItem) }
    foreach ($nckhMember in @($nckhItem) + $nckhMembers) {
        if ($nckhMember.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Cleanup rejects links and junctions.' }
    }
    $nckhFiles = @($nckhMembers | Where-Object { -not $_.PSIsContainer })
    $nckhInventory += [pscustomobject]@{
        path = $nckhResolved
        relative_path = $nckhResolved.Substring($nckhRootPrefix.Length).Replace('\', '/')
        files = $nckhFiles.Count
        bytes = [long](($nckhFiles | Measure-Object -Property Length -Sum).Sum)
        status = 'preview'
    }
}
$nckhManifest = [pscustomobject]@{ status = 'preview'; scope = $Scope; targets = $nckhInventory; errors = @() }
$nckhManifestPath = Join-Path $nckhReleaseState ("obsolete-" + $Scope + '.json')
$nckhManifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $nckhManifestPath -Encoding utf8

if ($Apply) {
    foreach ($nckhRow in $nckhInventory) {
        try {
            $nckhFinalPath = (Resolve-Path -LiteralPath $nckhRow.path).ProviderPath
            if ($nckhFinalPath -ne $nckhRow.path -or -not $nckhFinalPath.StartsWith($nckhRootPrefix, [StringComparison]::OrdinalIgnoreCase)) {
                throw 'Cleanup target identity changed after inventory.'
            }
            if ((Get-Item -LiteralPath $nckhFinalPath -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw 'Cleanup target became a link.'
            }
            Remove-Item -LiteralPath $nckhFinalPath -Recurse -Force
            $nckhRow.status = 'removed'
        } catch {
            $nckhRow.status = 'failed'
            $nckhManifest.errors += [pscustomobject]@{ path = $nckhRow.relative_path; reason = $_.Exception.Message }
        }
    }
    $nckhManifest.status = if ($nckhManifest.errors.Count) { 'partial' } else { 'pass' }
    $nckhManifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $nckhManifestPath -Encoding utf8
}
[pscustomobject]@{
    status = $nckhManifest.status
    targets = $nckhInventory.Count
    removed = @($nckhInventory | Where-Object status -EQ 'removed').Count
    files = [long](($nckhInventory | Measure-Object -Property files -Sum).Sum)
    bytes = [long](($nckhInventory | Measure-Object -Property bytes -Sum).Sum)
    errors = $nckhManifest.errors.Count
} | ConvertTo-Json
if ($nckhManifest.errors.Count) { exit 2 }
