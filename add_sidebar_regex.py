import re
import codecs

html_path = r"d:\Respaldo José Rugama\Escritorio\Tecnologico Nacional 2026\pages\centros-tecnologicos.html"

with codecs.open(html_path, "r", "utf-8") as f:
    html = f.read()

# 1. Add CSS
css_addition = """        @media (max-width: 767px) {
            .centros-hero {
                padding: 50px 0 70px;
            }

            .centros-hero h1 {
                font-size: 2rem;
            }
        }
        
        .active-dept {
            background-color: var(--primary-blue) !important;
            color: white !important;
            font-weight: bold;
            box-shadow: 0 4px 10px rgba(19, 88, 139, 0.2);
        }
        
        #departamentos-list .list-group-item:hover:not(.active-dept) {
            background-color: rgba(153, 223, 249, 0.2);
            color: var(--primary-blue);
            cursor: pointer;
        }
        
        #departamentos-list::-webkit-scrollbar {
            width: 6px;
        }
        #departamentos-list::-webkit-scrollbar-thumb {
            background-color: #cbd5e1;
            border-radius: 10px;
        }
    </style>"""

html = re.sub(r'        @media \(max-width: 767px\) \{\s*\.centros-hero \{\s*padding: 50px 0 70px;\s*\}\s*\.centros-hero h1 \{\s*font-size: 2rem;\s*\}\s*\}\s*</style>', css_addition, html, flags=re.DOTALL)

# 2. Modify Grid
grid_replacement = """    <section class="container mb-5 centros-grid">
        <div class="row g-4">
            <!-- Columna Izquierda: Filtro Departamentos -->
            <div class="col-lg-3">
                <div class="card border-0 shadow-sm rounded-4 position-sticky" style="top: 100px;">
                    <div class="card-header bg-white border-0 pt-4 pb-2 px-4 rounded-top-4">
                        <h5 class="fw-bold mb-0" style="color: var(--primary-blue);"><i class="bi bi-geo-alt-fill me-2"></i> Departamentos</h5>
                    </div>
                    <div class="card-body p-0 px-2 pb-3">
                        <ul class="list-group list-group-flush border-0" id="departamentos-list" style="max-height: 60vh; overflow-y: auto;">
                            <!-- Los departamentos se cargarán aquí -->
                        </ul>
                    </div>
                </div>
            </div>
            <!-- Columna Derecha: Cuadrícula Centros -->
            <div class="col-lg-9">
                <div class="row g-4" id="centros-container">
                    <!-- Los centros se cargarán dinámicamente aquí -->
                </div>
                <div id="pagination-info" class="pagination-info mt-5"></div>
                <div id="pagination-controls" class="pagination-container"></div>
            </div>
        </div>
    </section>"""

html = re.sub(r'<section class="container mb-5 centros-grid">\s*<div class="row g-4" id="centros-container">\s*<!-- Los centros se cargarán dinámicamente aquí -->\s*</div>\s*<div id="pagination-info" class="pagination-info"></div>\s*<div id="pagination-controls" class="pagination-container"></div>\s*</section>', grid_replacement, html, flags=re.DOTALL)

# 3. Add JS 1
js_replacement_1 = """            const container = document.getElementById('centros-container');
            const searchInput = document.getElementById('search-centros');
            const paginationControls = document.getElementById('pagination-controls');
            const paginationInfo = document.getElementById('pagination-info');
            const deptsList = document.getElementById('departamentos-list');

            const ITEMS_PER_PAGE = 12;
            let currentPage = 1;
            let currentData = [];
            let activeDept = 'todos';

            if (!container || !window.centrosData) {
                console.error("No se pudo cargar la información de los centros.");
                return;
            }

            // Renderiza la lista de departamentos y maneja los clicks
            function renderDepartamentos() {
                // Extraer ubicaciones únicas y ordenarlas alfabeticamente
                const depts = [...new Set(window.centrosData.map(c => c.ubicacion))].sort();
                
                deptsList.innerHTML = `
                    <li class="list-group-item border-0 active-dept" style="cursor: pointer; border-radius: 8px; margin: 2px 8px; transition: all 0.2s;" data-dept="todos">
                        <i class="bi bi-globe-americas me-2"></i> Todos los Departamentos
                    </li>
                `;
                
                depts.forEach(dept => {
                    deptsList.innerHTML += `
                        <li class="list-group-item border-0" style="cursor: pointer; border-radius: 8px; margin: 2px 8px; transition: all 0.2s;" data-dept="${dept}">
                            <i class="bi bi-geo-alt-fill me-2 text-muted"></i> ${dept}
                        </li>
                    `;
                });

                // Añadir event listeners a cada item
                deptsList.querySelectorAll('li').forEach(li => {
                    li.addEventListener('click', (e) => {
                        // Remover clase active de todos
                        deptsList.querySelectorAll('li').forEach(el => el.classList.remove('active-dept'));
                        // Añadir al clickeado
                        e.currentTarget.classList.add('active-dept');
                        
                        activeDept = e.currentTarget.getAttribute('data-dept');
                        filterData();
                    });
                });
            }

            // Filtro combinado de departamento y búsqueda
            function filterData() {
                const term = searchInput.value.toLowerCase();
                
                const filtered = window.centrosData.filter(c => {
                    const matchTerm = c.nombre.toLowerCase().includes(term) || c.ubicacion.toLowerCase().includes(term);
                    const matchDept = (activeDept === 'todos') ? true : (c.ubicacion === activeDept);
                    
                    return matchTerm && matchDept;
                });
                
                renderPage(filtered, 1);
            }"""

html = re.sub(r"const container = document\.getElementById\('centros-container'\);\s*const searchInput = document\.getElementById\('search-centros'\);\s*const paginationControls = document\.getElementById\('pagination-controls'\);\s*const paginationInfo = document\.getElementById\('pagination-info'\);\s*const ITEMS_PER_PAGE = 12;\s*let currentPage = 1;\s*let currentData = \[\];\s*if \(!container \|\| !window\.centrosData\) \{\s*console\.error\(\"No se pudo cargar la información de los centros\.\"\);\s*return;\s*\}", js_replacement_1, html, flags=re.DOTALL)

# 4. Add JS 2
js_replacement_2 = """            searchInput.addEventListener('input', () => {
                filterData();
            });

            // Initial render
            renderDepartamentos();
            filterData();"""

html = re.sub(r"searchInput\.addEventListener\('input', \(e\) => \{\s*const term = e\.target\.value\.toLowerCase\(\);\s*const filtered = window\.centrosData\.filter\(c =>\s*c\.nombre\.toLowerCase\(\)\.includes\(term\) \|\|\s*c\.ubicacion\.toLowerCase\(\)\.includes\(term\)\s*\);\s*renderPage\(filtered, 1\);\s*\}\);\s*// Initial render\s*renderPage\(window\.centrosData, 1\);", js_replacement_2, html, flags=re.DOTALL)


with codecs.open(html_path, "w", "utf-8") as f:
    f.write(html)

print("HTML modified successfully using regex!")
