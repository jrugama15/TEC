$root = "c:\Users\Jose\Desktop\Tecnologico Nacional 2026"

# 1. Create organized folders
$folders = @("$root\docs", "$root\scripts", "$root\static\core\img")
foreach ($f in $folders) {
    if (!(Test-Path $f)) { New-Item -ItemType Directory -Path $f | Out-Null; Write-Host "Created: $f" }
    else { Write-Host "Exists:  $f" }
}

# 2. Move documentation/reference files to docs/
$docFiles = @("WEB TecNacional.txt", "dummy.txt", "scraper.py")
foreach ($file in $docFiles) {
    $src = "$root\$file"
    $dst = "$root\docs\$file"
    if (Test-Path $src) {
        Move-Item $src $dst -Force
        Write-Host "Moved to docs/: $file"
    }
}

# 3. Move fix_navbar.ps1 from project root to scripts/
$src = "$root\fix_navbar.ps1"
if (Test-Path $src) {
    Move-Item $src "$root\scripts\fix_navbar.ps1" -Force
    Write-Host "Moved to scripts/: fix_navbar.ps1"
}

# 4. Delete the fix_navbar.ps1 left on the Desktop
$desktopScript = "c:\Users\Jose\Desktop\fix_navbar.ps1"
if (Test-Path $desktopScript) {
    Remove-Item $desktopScript -Force
    Write-Host "Deleted from Desktop: fix_navbar.ps1"
} else {
    Write-Host "Not found on Desktop (already gone): fix_navbar.ps1"
}

# 5. Move the lone logo inside logos/ subfolder up to img/ and remove empty logos/ subfolder
$logosDir = "$root\static\core\img\logos"
if (Test-Path $logosDir) {
    Get-ChildItem $logosDir -File | ForEach-Object {
        $dst = "$root\static\core\img\$($_.Name)"
        if (!(Test-Path $dst)) {
            Move-Item $_.FullName $dst -Force
            Write-Host "Merged logo: $($_.Name) -> static/core/img/"
        } else {
            Write-Host "Skipped (already exists at dest): $($_.Name)"
        }
    }
    # Remove empty logos/ dir
    $remaining = Get-ChildItem $logosDir
    if ($remaining.Count -eq 0) {
        Remove-Item $logosDir -Force
        Write-Host "Removed empty folder: static/core/img/logos/"
    } else {
        Write-Host "logos/ folder not empty, left as-is"
    }
}

Write-Host ""
Write-Host "=== Final structure ==="
Get-ChildItem $root | ForEach-Object { Write-Host "  $($_.Name)" }
