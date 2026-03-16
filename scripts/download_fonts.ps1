$fontsDir = "c:\Users\Jose\Desktop\Tecnologico Nacional 2026\static\core\css\fonts"
New-Item -ItemType Directory -Force -Path $fontsDir | Out-Null

$woff2Url = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/fonts/bootstrap-icons.woff2"
$woffUrl  = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/fonts/bootstrap-icons.woff"

Write-Host "Descargando bootstrap-icons.woff2..."
Invoke-WebRequest -Uri $woff2Url -OutFile "$fontsDir\bootstrap-icons.woff2" -UseBasicParsing
Write-Host "Descargando bootstrap-icons.woff..."
Invoke-WebRequest -Uri $woffUrl  -OutFile "$fontsDir\bootstrap-icons.woff"  -UseBasicParsing

Write-Host ""
Write-Host "=== Resultado ==="
Get-ChildItem $fontsDir | ForEach-Object {
    $kb = [Math]::Round($_.Length / 1024, 1)
    Write-Host "OK: $($_.Name) ($kb KB)"
}
