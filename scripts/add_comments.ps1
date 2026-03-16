$path = "c:\Users\Jose\Desktop\Tecnologico Nacional 2026\index.html"
$lines = [System.IO.File]::ReadAllLines($path, [System.Text.Encoding]::UTF8)

# Helper: insert comment BEFORE a given 0-based line index
function InsertBefore($arr, $idx, $comment) {
    $before = if ($idx -gt 0) { $arr[0..($idx-1)] } else { @() }
    $after  = $arr[$idx..($arr.Count-1)]
    return $before + @($comment) + $after
}

# We'll build a list of (searchString, comment) pairs and process them
# Each entry: @{ Find = "unique fragment in target line"; Comment = "<!-- COMMENT -->" }
$insertions = @(
    @{ Find = '<head>';                      Before = $false; Comment = '' },  # skip, already has context
    @{ Find = 'meta charset';               Before = $true;  Comment = '  <!-- ============================================================' + "`r`n" + '       TECNOLOGICO NACIONAL INATEC - index.html' + "`r`n" + '       Ultima modificacion: 2026' + "`r`n" + '       Estructura: HEAD > NAVBAR > HERO BANNER > CONTENIDO > FOOTER > SCRIPTS' + "`r`n" + '  ============================================================ -->' },
    @{ Find = 'bootstrap.min.css';          Before = $true;  Comment = '  <!-- ── ESTILOS CSS: se cargan en orden de prioridad ── -->' },
    @{ Find = 'inicio.css';                 Before = $false; Comment = '  <!-- Fin de estilos CSS -->' },
    @{ Find = '<title>';                    Before = $true;  Comment = '  <!-- ── SEO: titulo y descripcion para motores de busqueda ── -->' },
    @{ Find = "Modern responsive navbar";   Before = $true;  Comment = '  <!-- ==========================================================' + "`r`n" + '       NAVBAR (Barra de Navegacion)' + "`r`n" + '       - Fijo en la parte superior (fixed-top)' + "`r`n" + '       - Fondo azul degradado que coincide con el banner' + "`r`n" + '       - Responsive: hamburguesa en movil, links en desktop' + "`r`n" + '       - Para cambiar colores: busca #0a3d6b y #14578b en el <style>' + "`r`n" + '       - Para agregar enlaces: busca <ul class="navbar-nav ms-auto">' + "`r`n" + '  =========================================================== -->' },
    @{ Find = 'HERO BANNER PRINCIPAL';      Before = $true;  Comment = '  <!-- ==========================================================' + "`r`n" + '       HERO BANNER PRINCIPAL' + "`r`n" + '       - Imagen de fondo: static/core/img/Construyo_mi_sueno...jpeg' + "`r`n" + '       - Para cambiar la imagen: modifica la URL en el <style> #myCarousel' + "`r`n" + '       - Alturas: 420px (desktop) / 280px (tablet) / 180px (movil)' + "`r`n" + '       - El margin-top compensa la altura del navbar fijo' + "`r`n" + '  =========================================================== -->' },
    @{ Find = 'id="typewriter-section"';    Before = $true;  Comment = '    <!-- ── SECCION: Animacion de texto "TECNOLOGICO" (efecto maquina de escribir) ── -->' },
    @{ Find = 'oferta_contenedor';          Before = $true;  Comment = '    <!-- ==========================================================' + "`r`n" + '         SECCION: OFERTA FORMATIVA' + "`r`n" + '         - Buscador de carreras con fondo imagen' + "`r`n" + '         - Para cambiar la imagen de fondo: modifica background-image en el style' + "`r`n" + '    =========================================================== -->' },
    @{ Find = 'container-fluid.*eeeeee';    Before = $true;  Comment = '    <!-- ==========================================================' + "`r`n" + '         SECCION: ESTADISTICAS + PLATAFORMAS VIRTUALES + NOTICIAS + VIDEOS' + "`r`n" + '         Contiene (en orden):' + "`r`n" + '           1. Tarjetas estadisticas (67 Carreras, 46 Centros)' + "`r`n" + '           2. Carrusel de Plataformas Virtuales (Swiper)' + "`r`n" + '           3. Noticias recientes (3 tarjetas)' + "`r`n" + '           4. Ultimos Videos (iframe YouTube)' + "`r`n" + '           5. Proximos Eventos' + "`r`n" + '           6. Multimedia (podcast, programas, biblioteca, galerias)' + "`r`n" + '    =========================================================== -->' },
    @{ Find = 'Pie_de_sitio_web.png';       Before = $true;  Comment = '    <!-- ── IMAGEN DECORATIVA: Pie de sitio (banda grafica inferior) ── -->' },
    @{ Find = '<footer>';                   Before = $true;  Comment = '  <!-- ==========================================================' + "`r`n" + '       FOOTER (Pie de Pagina)' + "`r`n" + '       - Logo INATEC + Datos de contacto (izquierda)' + "`r`n" + '       - Links del sitio + Redes sociales (centro)' + "`r`n" + '       - Logo Gobierno + Formulario suscripcion (derecha)' + "`r`n" + '       - Barra de copyright (fondo azul)' + "`r`n" + '  =========================================================== -->' },
    @{ Find = '</footer>';                  Before = $false; Comment = '  <!-- Fin del Footer -->' },
    @{ Find = 'jquery-3.6.0.min.js';        Before = $true;  Comment = '  <!-- ==========================================================' + "`r`n" + '       SCRIPTS JAVASCRIPT (al final del body para no bloquear el render)' + "`r`n" + '       Orden importante:' + "`r`n" + '         1. jQuery (requerido por Bootstrap y funciones propias)' + "`r`n" + '         2. functionLoader.js (loader de pagina)' + "`r`n" + '         3. buscador.js (logica del buscador de carreras)' + "`r`n" + '         4. bootstrap.bundle.min.js (componentes Bootstrap: modales, dropdowns)' + "`r`n" + '         5. aos.js (animaciones al hacer scroll)' + "`r`n" + '         6. swiper-bundle.min.js (carrusel de plataformas)' + "`r`n" + '         7. functionBase.js (funciones generales del sitio)' + "`r`n" + '  =========================================================== -->' },
    @{ Find = "AOS.init";                   Before = $true;  Comment = '  <!-- ── Inicializacion de AOS (animaciones) y deteccion de dispositivo ── -->' },
    @{ Find = "Swiper configuracion";       Before = $true;  Comment = '  <!-- ── Configuracion del carrusel Swiper (plataformas virtuales) ── -->' },
    @{ Find = "google_translate_element.*display:none"; Before = $true; Comment = '  <!-- ==========================================================' + "`r`n" + '       GOOGLE TRANSLATE (carga diferida)' + "`r`n" + '       Se carga despues del evento "load" para no bloquear la pagina' + "`r`n" + '  =========================================================== -->' }
)

# Process each insertion
foreach ($item in $insertions) {
    if (-not $item.Comment -or -not $item.Find) { continue }
    
    # Find matching line
    $found = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match [regex]::Escape($item.Find) -or $lines[$i] -match $item.Find) {
            $found = $i
            break
        }
    }
    
    if ($found -lt 0) {
        Write-Host "NOT FOUND: $($item.Find)"
        continue
    }
    
    $insertAt = if ($item.Before) { $found } else { $found + 1 }
    
    # Split comment into lines
    $commentLines = $item.Comment -split "`r`n"
    
    $before = if ($insertAt -gt 0) { $lines[0..($insertAt - 1)] } else { @() }
    $after  = $lines[$insertAt..($lines.Count - 1)]
    $lines  = $before + $commentLines + $after
    
    Write-Host "Added comment at line $($insertAt + 1): '$($item.Find.Substring(0, [Math]::Min(40,$item.Find.Length)))...'"
}

[System.IO.File]::WriteAllLines($path, $lines, (New-Object System.Text.UTF8Encoding $false))
Write-Host ""
Write-Host "Done! Total lines: $($lines.Count)"
