$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Venv = Join-Path $Root ".venv"
$Python = Join-Path $Venv "Scripts\python.exe"

Set-Location $Root

function Assert-LastExitCode {
    param([Parameter(Mandatory = $true)][string]$Step)

    if ($LASTEXITCODE -ne 0) {
        throw "$Step failed with exit code $LASTEXITCODE"
    }
}

function Remove-WorkspaceChild {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path $Path)) {
        return
    }

    $ResolvedRoot = (Resolve-Path $Root).Path
    $ResolvedPath = (Resolve-Path $Path).Path
    $Prefix = $ResolvedRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    if (-not $ResolvedPath.StartsWith($Prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove path outside workspace: $ResolvedPath"
    }

    Remove-Item -LiteralPath $ResolvedPath -Recurse -Force
}

if (-not (Test-Path $Python)) {
    py -3.12 -m venv $Venv
    Assert-LastExitCode "Create virtual environment"
}

& $Python -m pip install --upgrade pip
Assert-LastExitCode "Upgrade pip"
& $Python -m pip install -r requirements.txt
Assert-LastExitCode "Install requirements"
& $Python -m pytest -q
Assert-LastExitCode "Run tests"

Remove-WorkspaceChild (Join-Path $Root "build")
Remove-WorkspaceChild (Join-Path $Root "dist")

$AppName = "Winlinez-Revival"
$Version = "1.0.2"
$RepoUrl = "https://github.com/kylefu8/Winlinez-Revival"
$IconPath = Join-Path $Root "assets\winlinez-icon.ico"
$IconPngPath = Join-Path $Root "assets\winlinez-icon.png"
$PortableDir = Join-Path $Root "dist\$AppName"
$ExePath = Join-Path $PortableDir "$AppName.exe"
$ZipPath = Join-Path $Root "dist\$AppName-portable.zip"
$SpecPath = Join-Path $Root "$AppName.spec"

Remove-Item -LiteralPath (Join-Path $Root "Winlinez.spec") -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $SpecPath -Force -ErrorAction SilentlyContinue

& $Python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name $AppName `
    --icon $IconPath `
    --add-data "$IconPngPath;assets" `
    --distpath $PortableDir `
    --paths src `
    run_winlinez.py
Assert-LastExitCode "Build executable"
Remove-Item -LiteralPath $SpecPath -Force -ErrorAction SilentlyContinue

$Readme = @"
Winlinez Revival Portable
=========================

Version: $Version
GitHub: $RepoUrl

Run Winlinez-Revival.exe to play. It is a single-file portable build and does not need an installer or Python.

This is a modern portable remake made because the old Winlinez no longer runs reliably on newer Windows systems.

Controls:
- Click a ball, then click an empty destination.
- Click the restart button to start a new game.
- Click the quit button to exit.
- N or F2 starts a new game.
- U or Backspace reverts the last valid move.
- Esc quits.

The best score is stored beside this exe as winlinez_high_score.json. Copy that file too only if you want to keep the record.
"@
Set-Content -LiteralPath (Join-Path $PortableDir "README.txt") -Value $Readme -Encoding UTF8

Compress-Archive -Path (Join-Path $PortableDir "*") -DestinationPath $ZipPath -Force

Write-Host ""
Write-Host "Portable build ready:"
Write-Host $ExePath
Write-Host $ZipPath
