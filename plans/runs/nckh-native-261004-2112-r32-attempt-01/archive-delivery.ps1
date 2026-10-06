$ErrorActionPreference = 'Stop'
$nckhRun = [System.IO.Path]::GetFullPath($PSScriptRoot)
$nckhContext = Get-Content -LiteralPath (Join-Path $nckhRun 'delivery-context.json') -Raw | ConvertFrom-Json
if ($nckhContext.status -ne 'built') { throw 'Build checkpoint is incomplete.' }
$nckhOutside = [System.IO.Path]::GetFullPath($nckhContext.outside)
$nckhAllowed = [System.IO.Path]::GetFullPath('C:/Users/USER\.codex\visualizations\2026\10\04\01a104fc-f969-7f43-b1e0-1a6774f0e0c8')
if (-not $nckhOutside.StartsWith($nckhAllowed + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'Extraction root escaped the owned workspace.'
}
if (-not (Test-Path -LiteralPath (Join-Path $nckhOutside 'owned-attempt.json'))) { throw 'Owned attempt marker is missing.' }
$nckhArchiveRoot = Join-Path $nckhRun 'archives'
if (Test-Path -LiteralPath $nckhArchiveRoot) { throw 'Preserve the existing archive attempt.' }
New-Item -ItemType Directory -Path $nckhArchiveRoot | Out-Null
$nckhRows = @()
try {
    foreach ($nckhVariant in $nckhContext.variants) {
        foreach ($nckhHost in $nckhContext.hosts) {
            $nckhBundle = Join-Path $nckhRun ("build\" + $nckhVariant + '\' + $nckhHost)
            $nckhZip = Join-Path $nckhArchiveRoot ($nckhVariant + '-' + $nckhHost + '.zip')
            $nckhExtracted = [System.IO.Path]::GetFullPath((Join-Path $nckhOutside ("extracted\" + $nckhVariant + '\' + $nckhHost)))
            if (-not $nckhExtracted.StartsWith($nckhOutside + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
                throw 'Expanded path escaped the owned attempt.'
            }
            if ((Test-Path -LiteralPath $nckhZip) -or (Test-Path -LiteralPath $nckhExtracted)) {
                throw 'Archive or extraction destination already exists.'
            }
            $nckhChildren = @(Get-ChildItem -LiteralPath $nckhBundle -Force | Select-Object -ExpandProperty FullName)
            Compress-Archive -LiteralPath $nckhChildren -DestinationPath $nckhZip
            New-Item -ItemType Directory -Path $nckhExtracted -Force | Out-Null
            Expand-Archive -LiteralPath $nckhZip -DestinationPath $nckhExtracted
            if (-not (Test-Path -LiteralPath (Join-Path $nckhExtracted 'manifest.json'))) {
                throw 'Extraction has no root manifest.'
            }
            $nckhRows += [PSCustomObject]@{
                variant = $nckhVariant
                host = $nckhHost
                archive = $nckhZip
                archive_sha256 = (Get-FileHash -LiteralPath $nckhZip -Algorithm SHA256).Hash.ToLowerInvariant()
                extracted = $nckhExtracted
                status = 'archived-and-extracted-unverified'
            }
            Write-Output ('archive ' + $nckhVariant + '-' + $nckhHost + ': extracted')
        }
    }
    $nckhResult = [PSCustomObject]@{status='pass'; source_lock_hash=$nckhContext.source_lock_hash; artifacts=$nckhRows}
    $nckhJson = $nckhResult | ConvertTo-Json -Depth 8
    [System.IO.File]::WriteAllText((Join-Path $nckhRun 'archive-summary.json'), $nckhJson, [System.Text.UTF8Encoding]::new($false))
} catch {
    $nckhFailure = [PSCustomObject]@{status='fail'; error=$_.Exception.Message; artifacts=$nckhRows}
    [System.IO.File]::WriteAllText((Join-Path $nckhRun 'archive-failure.json'), ($nckhFailure | ConvertTo-Json -Depth 8), [System.Text.UTF8Encoding]::new($false))
    throw
}
