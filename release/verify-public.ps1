param(
    [Parameter(Mandatory = $true)]
    [string]$PublicRoot,
    [string]$Allowlist = ""
)

$ErrorActionPreference = "Stop"
$PublicRoot = (Resolve-Path -LiteralPath $PublicRoot).Path
if (-not $Allowlist) {
    $Allowlist = Join-Path $PSScriptRoot "public-allowlist.txt"
}
$Allowlist = (Resolve-Path -LiteralPath $Allowlist).Path

$allowed = Get-Content -LiteralPath $Allowlist |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -and -not $_.StartsWith("#") } |
    ForEach-Object { $_.Replace("\", "/").TrimEnd("/") }

if (-not $allowed) {
    throw "The public allowlist is empty: $Allowlist"
}

$unexpected = @()
$forbidden = @()
$rootPrefix = $PublicRoot.TrimEnd([char[]]@('\', '/')) + [System.IO.Path]::DirectorySeparatorChar
Get-ChildItem -LiteralPath $PublicRoot -Recurse -File -Force |
    Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' } |
    ForEach-Object {
        $relative = $_.FullName.Substring($rootPrefix.Length).Replace("\", "/")
        $isAllowed = $false
        foreach ($entry in $allowed) {
            if ($relative -eq $entry -or $relative.StartsWith("$entry/")) {
                $isAllowed = $true
                break
            }
        }
        if (-not $isAllowed) {
            $unexpected += $relative
        }
        if ($relative -eq "AGENTS.md" -or
            $relative.StartsWith(".claude/") -or
            $relative.StartsWith("docs-developer/") -or
            $relative.StartsWith("release/") -or
            $relative.StartsWith("examples/task3_3_co2_extended/")) {
            $forbidden += $relative
        }
    }

if ($unexpected) {
    throw "Public tree contains paths outside the allowlist:`n$($unexpected -join "`n")"
}
if ($forbidden) {
    throw "Public tree contains private-only paths:`n$($forbidden -join "`n")"
}

$leakPattern = 'auto_phreeqc_proj|C:\\Users\\songsongr|TeamCreate|docs-developer'
$leaks = & rg -n --hidden --glob '!.git/**' --glob '!.gitignore' -e $leakPattern $PublicRoot
if ($LASTEXITCODE -eq 0) {
    throw "Public tree contains private-development content:`n$($leaks -join "`n")"
}
if ($LASTEXITCODE -gt 1) {
    throw "Could not scan the public tree for private-development content."
}

Write-Host "Public release verification passed: $PublicRoot"
