$path = "c:\Users\Jose\Desktop\Tecnologico Nacional 2026\index.html"
$c = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# ── 1. HEAD: quitar Bootstrap Icons CDN duplicado (ya existe local)
$c = $c -replace '\r?\n  <link href="https://cdn\.jsdelivr\.net/npm/bootstrap-icons@[^"]+/font/bootstrap-icons\.css" rel="stylesheet" />', ''

# ── 2. HEAD: quitar Swiper CSS de CDN externa (ya existe local swiper-bundle.min.css)
$c = $c -replace '\r?\n  <link href="https://cdnjs\.cloudflare\.com/ajax/libs/Swiper/[^"]+/css/swiper\.css" rel="stylesheet" />', ''

# ── 3. HEAD: quitar swiper.css redundante (swiper-bundle.min.css lo incluye todo)
$c = $c -replace '\r?\n  <link href="static/core/css/swiper\.css" rel="stylesheet" />', ''

# ── 4. HEAD: quitar animate.min.css (71 KB de animaciones no usadas en el HTML actual)
$c = $c -replace '\r?\n  <link href="static/core/css/animate\.min\.css" rel="stylesheet" />', ''

# ── 5. HEAD: quitar fakeLoader CSS (vamos a quitar el loader completamente)
$c = $c -replace '\r?\n  <link href="static/core/css/fakeLoader\.min\.css" rel="stylesheet" />', ''

# ── 6. HEAD: quitar Google Translate del <head> y reemplazar por carga lazy al final del body
$googleTranslateHead = @"

  <!-- Google Translate -->
  <script type="text/javascript">
    function googleTranslateElementInit() {
      new google.translate.TranslateElement({
        pageLanguage: 'es',
        autoDisplay: false
      }, 'google_translate_element');
    }
  </script>
  <script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
"@
$c = $c.Replace($googleTranslateHead, '')

# ── 7. BODY: quitar el <div class="fakeloader"> duplicado al inicio del body
$c = $c -replace '  <div class="fakeloader"></div>\r?\n  <!-- INICIO HEADER -->', '  <!-- INICIO HEADER -->'

# ── 8. BODY: quitar el <div id="container-base-menu-one"> vacío
$c = $c -replace '  <div id="container-base-menu-one">\r?\n  </div>\r?\n', ''

# ── 9. BODY: quitar Facebook Customer Chat plugin (bloquea carga, requiere SDK externo)
$c = [regex]::Replace($c, '(?s)  <!-- PLUGIN DE CHAT -->\r?\n  <div attribution="install_email".*?</div>\r?\n', '')

# ── 10. BODY: quitar el overlay SVG de loading (reemplazar con CSS spinner ligero en el fakeloader.js de abajo)
$c = [regex]::Replace($c, '(?s)  <div id="overlay">.*?</div>\r?\n  <script src="static/core/js/jquery', '  <script src="static/core/js/jquery')

# ── 11. SCRIPTS: quitar fakeLoader.min.js (quitamos el loader completamente)
$c = $c -replace '\r?\n  <script src="static/core/js/fakeLoader\.min\.js"></script>', ''

# ── 12. SCRIPTS: quitar Swiper CDN externa (ya existe swiper-bundle.min.js local)
$c = $c -replace '\r?\n  <script src="https://cdnjs\.cloudflare\.com/ajax/libs/Swiper/[^"]+/js/swiper\.js"></script>', ''

# ── 13. SCRIPTS: quitar swiper.js local redundante (swiper-bundle.min.js incluye todo)
$c = $c -replace '\r?\n  <script src="static/core/js/swiper\.js"></script>', ''

# ── 14. SCRIPTS: quitar alertify.js (no se usa en el HTML visible)
$c = $c -replace '\r?\n  <script src="static/core/js/alertify\.js"></script>', ''

# ── 15. BODY: quitar el <div class="fakeloader"> duplicado al FINAL del body (línea 1023)
$c = $c -replace '\r?\n  <div class="fakeloader"></div>\r?\n</body>', "`r`n</body>"

# ── 16. Agregar Google Translate lazy + ocultarLoader CSS simple antes de </body>
$lazyScripts = @"

  <!-- Google Translate: carga lazy después de que la página sea interactiva -->
  <div id="google_translate_element" style="display:none;"></div>
  <script>
    window.addEventListener('load', function() {
      var s = document.createElement('script');
      s.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
      document.body.appendChild(s);
    });
    function googleTranslateElementInit() {
      new google.translate.TranslateElement({ pageLanguage: 'es', autoDisplay: false }, 'google_translate_element');
    }
  </script>
"@

# Insert before </body>
$c = $c.Replace("`r`n</body>", "$lazyScripts`r`n</body>")

# ── Write result
[System.IO.File]::WriteAllText($path, $c, (New-Object System.Text.UTF8Encoding $false))

Write-Host "Optimizacion completa."
Write-Host "Tamano final: $([Math]::Round((Get-Item $path).length / 1KB, 1)) KB"

# Quick checks
if ($c -match 'animate.min.css')          { Write-Host "WARN: animate.min.css still present" }  else { Write-Host "OK: animate.min.css removed" }
if ($c -match 'fakeLoader.min.css')       { Write-Host "WARN: fakeLoader.min.css still present" } else { Write-Host "OK: fakeLoader CSS removed" }
if ($c -match 'cdnjs.cloudflare.com')     { Write-Host "WARN: CDN swiper still present" }         else { Write-Host "OK: CDN swiper removed" }
if ($c -match 'cdn.jsdelivr.net')         { Write-Host "WARN: CDN icons still present" }           else { Write-Host "OK: CDN icons removed" }
if ($c -match 'fb-customerchat')          { Write-Host "WARN: Facebook chat still present" }        else { Write-Host "OK: Facebook chat removed" }
if ($c -match 'id="overlay"')             { Write-Host "WARN: overlay SVG still present" }          else { Write-Host "OK: overlay SVG removed" }
if ($c -match 'fakeLoader.min.js')        { Write-Host "WARN: fakeLoader.min.js still present" }   else { Write-Host "OK: fakeLoader JS removed" }
if ($c -match 'alertify.js')              { Write-Host "WARN: alertify.js still present" }          else { Write-Host "OK: alertify.js removed" }
