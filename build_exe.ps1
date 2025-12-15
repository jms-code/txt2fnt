# Build txt2fnt into a Windows EXE using PyInstaller
# Usage: Open PowerShell (x86/x64 matching your Python) and run:
#   ./build_exe.ps1
# This script will create a single-file EXE in the `dist/` folder.

param(
    [switch]$OneFile = $true
)

# Ensure pyinstaller is available
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller not found. Installing into the active environment..." -ForegroundColor Yellow
    python -m pip install --upgrade pyinstaller
}

$projRoot = (Get-Location).Path
$entry = "txt2fnt.py"

# Files / folders that need to be bundled as data
# On Windows the separator is ';' (on *nix it's ':')
$addDataArgs = @(
    "in;in",
    "_tools_;_tools_",
    "workspace;workspace"
)

# Build an argument array so each --add-data is a separate argument
$addDataFlags = $addDataArgs | ForEach-Object { @("--add-data", $_) } | Select-Object -ExpandProperty @{Name='Value'} -ErrorAction SilentlyContinue

# Fallback simpler construction if the above is not supported on older PowerShell
if (-not $addDataFlags) {
    $addDataFlags = @()
    foreach ($a in $addDataArgs) { $addDataFlags += "--add-data"; $addDataFlags += $a }
}

if ($OneFile) {
    $pyArgs = @("--clean", "--onefile", "--console") + $addDataFlags + @($entry)
} else {
    $pyArgs = @("--clean", "--onedir", "--console") + $addDataFlags + @($entry)
}

pyinstaller @pyArgs

Write-Host "Build finished. See dist\ for the result." -ForegroundColor Green
