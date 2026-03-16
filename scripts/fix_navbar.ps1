$path = "c:\Users\Jose\Desktop\Tecnologico Nacional 2026\index.html"
$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# Check if accents are correct
$lines = $content -split "`n"
for ($i = 78; $i -le 108; $i++) {
    if ($lines[$i] -match "OFERTA|dropdown-toggle|nav-link") {
        Write-Host "Line $($i+1): $($lines[$i].Trim())"
    }
}

# Count occurrences of broken sequences
$broken = ($content -split "Ã‰").Count - 1
Write-Host "Remaining broken sequences (E-acute): $broken"
$broken2 = ($content -split "Ã`"").Count - 1
Write-Host "Remaining broken sequences (O-acute): $broken2"
