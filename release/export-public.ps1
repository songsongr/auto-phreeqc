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
$publicFiles = Join-Path $PSScriptRoot "public-files"

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

# These files are purpose-built public replacements for private root-level
# instructions. They are copied after the archive rather than read from the
# development checkout.
$injectedPaths = @(
    "AGENTS.md",
    "CLAUDE.md",
    ".agents/skills/phreeqc-auto/SKILL.md"
)
$archivePaths = $paths | Where-Object { $_ -notin $injectedPaths }

$archive = Join-Path ([System.IO.Path]::GetTempPath()) (
    "auto-phreeqc-public-" + [guid]::NewGuid().ToString("N") + ".zip"
)
try {
    & git -C $SourceRoot archive --format=zip "--output=$archive" $Revision -- $archivePaths
    if ($LASTEXITCODE -ne 0) {
        throw "git archive failed for revision $Revision"
    }
    Expand-Archive -LiteralPath $archive -DestinationPath $DestinationRoot -Force
    if (Test-Path -LiteralPath $publicFiles) {
        Get-ChildItem -LiteralPath $publicFiles -Force |
            Copy-Item -Destination $DestinationRoot -Recurse -Force
    }
    & $verifyScript -PublicRoot $DestinationRoot -Allowlist $allowlist
} finally {
    if (Test-Path -LiteralPath $archive) {
        Remove-Item -LiteralPath $archive -Force
    }
}

Write-Host "Exported public release tree to $DestinationRoot"
