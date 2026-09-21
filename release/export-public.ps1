param(
    [Parameter(Mandatory = $true)]
    [string]$DestinationRoot,
    [string]$SourceRoot = "",
    [string]$Revision = "HEAD"
)

$ErrorActionPreference = "Stop"
if (-not $SourceRoot) {
    $SourceRoot = Split-Path -Parent $PSScriptRoot
}
$SourceRoot = (Resolve-Path -LiteralPath $SourceRoot).Path
$allowlist = Join-Path $PSScriptRoot "public-allowlist.txt"
$verifyScript = Join-Path $PSScriptRoot "verify-public.ps1"

if (-not (Test-Path -LiteralPath $DestinationRoot)) {
    New-Item -ItemType Directory -Path $DestinationRoot | Out-Null
}
$DestinationRoot = (Resolve-Path -LiteralPath $DestinationRoot).Path

$existing = Get-ChildItem -LiteralPath $DestinationRoot -Force |
    Where-Object { $_.Name -ne ".git" }
if ($existing) {
    throw "Destination must be empty apart from .git: $DestinationRoot"
}

$paths = Get-Content -LiteralPath $allowlist |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -and -not $_.StartsWith("#") }
if (-not $paths) {
    throw "The public allowlist is empty: $allowlist"
}

$archive = Join-Path ([System.IO.Path]::GetTempPath()) (
    "auto-phreeqc-public-" + [guid]::NewGuid().ToString("N") + ".zip"
)
try {
    & git -C $SourceRoot archive --format=zip "--output=$archive" $Revision -- $paths
    if ($LASTEXITCODE -ne 0) {
        throw "git archive failed for revision $Revision"
    }
    Expand-Archive -LiteralPath $archive -DestinationPath $DestinationRoot -Force
    & $verifyScript -PublicRoot $DestinationRoot -Allowlist $allowlist
} finally {
    if (Test-Path -LiteralPath $archive) {
        Remove-Item -LiteralPath $archive -Force
    }
}

Write-Host "Exported public release tree to $DestinationRoot"
