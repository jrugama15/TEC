# Footer igual al de index.html pero con rutas relativas (../) para pages/
$footerPages = @"

  <!-- FOOTER -->
  <footer>
    <div class="container-fluid base_footer">
      <div class="row pt-5">
        <div class="container text-center">
          <img class="mx-3" src="../static/core/img/logo_ci_2022.png" style="width: 12%" />
          <img class="mx-3" src="../static/core/img/logo_mid_2022.png" style="width: 9%" />
          <img class="mx-3" src="../static/core/img/logo_in_2022.png" style="width: 12%" />
        </div>
        <div class="row">
          <div class="col-xs-1 col-sm-3 text-start" style="margin-left: 0px">
            <div class="row">
              <div class="col"><img src="../static/core/img/logo_inatec_2022.png"
                  style="margin-left: 10%; height: 100px; width:auto" /></div>
            </div>
            <div class="row">
              <div class="col col_contactanos">
                <div>
                  <h5 class="text-light"><strong>Contactanos</strong></h5>
                  <h6 class="text-light enlace">Centro Cívico Zumen, Frente al Hospital Bertha Calderón, Managua</h6>
                  <h6 class="text-light enlace"><i></i>Atención al Protagonista: 2253-8888</h6>
                  <h6 class="text-light enlace"><i></i>Planta Central: 2253-8830</h6>
                </div>
              </div>
            </div>
          </div>
          <div class="col-xs-1 col-sm-6 container_links">
            <div class="row">
              <div class="col">
                <a href="../index.html">
                  <h6 class="text-light enlace"><i></i><span class="pesta_footer">&gt;</span> INICIO</h6>
                </a>
                <a href="nosotros.html">
                  <h6 class="text-light enlace"><i></i><span class="pesta_footer">&gt;</span> NOSOTROS</h6>
                </a>
                <a href="oferta-academica.html">
                  <h6 class="text-light enlace"><i></i><span class="pesta_footer">&gt;</span> OFERTA FORMATIVA</h6>
                </a>
                <a href="centros-tecnologicos.html">
                  <h6 class="text-light enlace"><i></i><span class="pesta_footer">&gt;</span> CENTROS TECNOLOGICOS</h6>
                </a>
                <a href="empresas.html">
                  <h6 class="text-light enlace"><i></i><span class="pesta_footer">&gt;</span> EMPRESAS</h6>
                </a>
              </div>
              <div class="col">
                <a href="https://serviciosenlinea.tecnacional.edu.ni/">
                  <h6 class="text-light enlace"><i></i><span class="pesta_footer">&gt;</span> SERVICIOS EN LINEA</h6>
                </a>
                <a href="galeria.html">
                  <h6 class="text-light enlace"><i></i><span class="pesta_footer">&gt;</span> GALERIAS FOTOGRAFICAS</h6>
                </a>
                <a href="boletines.html">
                  <h6 class="text-light enlace"><i></i><span class="pesta_footer">&gt;</span> BOLETINES INFORMATIVOS</h6>
                </a>
                <a href="eventos.html">
                  <h6 class="text-light enlace"><i></i><span class="pesta_footer">&gt;</span> EVENTOS</h6>
                </a>
                <a href="https://campus.tecnacional.edu.ni/">
                  <h6 class="text-light enlace"><i></i><span class="pesta_footer">&gt;</span> ENTORNOS VIRTUALES</h6>
                </a>
              </div>
              <div class="col">
                <a href="https://campus.tecnacional.edu.ni/">
                  <h6 class="text-light"> Plataformas Educativas</h6>
                </a>
                <a href="innovatec.html">
                  <h6 class="text-light pesta_innovatec"> Innovatec</h6>
                </a><br />
                <a href="podcast.html">
                  <h6 class="text-light pesta_podcast"> Podcast TEC</h6>
                </a><br />
                <a href="campus-virtual.html">
                  <h6 class="text-light pesta_campus"> Campus Virtual</h6>
                </a><br />
              </div>
            </div>
            <div class="row justify-content-center container_icons_links">
              <ul class="icons_redes_sociales d-flex gap-3 justify-content-center list-unstyled mb-0 mt-3 align-items-center">
                <li title="Facebook"><a href="https://www.facebook.com/TecNacional/" target="_blank" class="text-white fs-4"><i class="bi-facebook"></i></a></li>
                <li title="Twitter"><a href="https://twitter.com/TecNacional" target="_blank" class="text-white fs-4"><i class="bi-twitter"></i></a></li>
                <li title="Instagram"><a href="https://www.instagram.com/tecnacional/" target="_blank" class="text-white fs-4"><i class="bi-instagram"></i></a></li>
                <li title="YouTube"><a href="https://www.youtube.com/c/TecNacional" target="_blank" class="text-white fs-4"><i class="bi-youtube"></i></a></li>
                <li title="Tiktok"><a href="https://www.tiktok.com/@tecnacional" target="_blank" class="text-white fs-4"><i class="bi-tiktok"></i></a></li>
              </ul>
            </div>
          </div>
          <div class="col-xs-1 col-sm-3 text-end">
            <img src="../static/core/img/logo_gobierno.png" style="height: 142px; margin-right: 10%; margin-top: -12px" />
            <div class="row">
              <div class="col text-start">
                <p class="label_correo">Solicitá Información</p>
                <div class="input-group mb-3">
                  <input class="input_correo" placeholder="Ingresá tu Correo Electrónico" style="border-radius: 20px" />
                  <span class="input-group-text" id="btn-suscribirse"
                    style="cursor:pointer; background-color:#87c440; color: white;"
                    title="Suscribirse para recibir información">Suscríbete</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="row"></div>
          <div class="row text-center" style="color: white">
            <h6>Capacitación y Educación Técnica, Gratuita y de Calidad</h6>
          </div>
        </div>
        <div class="row text-center" style="background-color: #0a80b9; color: white">
          <h6 style="margin: 0px; padding: 10px;">Todos los Derechos Reservados Instituto Nacional Tecnológico - INATEC - 2026</h6>
        </div>
      </div>
    </div>
  </footer>
"@

$pagesDir = "D:\Respaldo José Rugama\Escritorio\Tecnologico Nacional 2026\pages"
$pages = Get-ChildItem -Path $pagesDir -Filter "*.html"

$updated = 0
$skipped = 0

foreach ($page in $pages) {
    $content = [System.IO.File]::ReadAllText($page.FullName, [System.Text.Encoding]::UTF8)
    
    # Encontrar el inicio del footer y el cierre de body
    $footerStart = $content.IndexOf("<footer")
    $bodyEnd = $content.LastIndexOf("</body>")
    
    if ($footerStart -lt 0 -or $bodyEnd -lt 0) {
        Write-Host "SKIP (no footer/body): $($page.Name)"
        $skipped++
        continue
    }
    
    # Tomar todo lo que hay antes del footer
    $before = $content.Substring(0, $footerStart)
    # Tomar solo los scripts que hay entre </footer> y </body>
    $afterFooterIdx = $content.IndexOf("</footer>", $footerStart)
    if ($afterFooterIdx -lt 0) {
        Write-Host "SKIP (no </footer>): $($page.Name)"
        $skipped++
        continue
    }
    $afterFooter = $content.Substring($afterFooterIdx + 9, $bodyEnd - ($afterFooterIdx + 9))
    
    # Construir el nuevo contenido
    $newContent = $before + $footerPages + $afterFooter + "</body>`r`n</html>"
    [System.IO.File]::WriteAllText($page.FullName, $newContent, [System.Text.Encoding]::UTF8)
    Write-Host "OK: $($page.Name)"
    $updated++
}

Write-Host ""
Write-Host "Actualizadas: $updated | Omitidas: $skipped"
