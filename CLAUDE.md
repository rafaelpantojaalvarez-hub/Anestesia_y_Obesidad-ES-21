# Instrucciones para Claude (leer al iniciar un chat nuevo)

Este repositorio contiene el libro **Anestesia y obesidad** (español) y **Anesthesia and Obesity** (inglés), en PDF. El autor (Dr. Rafael Pantoja) pide cambios por chat; se aplican **siempre en ambos libros**.

## Versión de trabajo
- Archivos vigentes: `Anestesia_y_Obesidad_ES_vNN.pdf` y `Anesthesia_and_Obesity_EN_vNN.pdf` (hoy **v39**; ver `README.md` para el número y el historial).
- Trabajar SIEMPRE sobre la última versión. No usar versiones anteriores.

## Flujo obligatorio por cada cambio
1. Aplicar el cambio en ES y EN sobre la última versión.
2. Guardar como versión NN+1 (`..._v(NN+1).pdf`, ambos idiomas), **eliminar** los PDF de la versión anterior (`git rm`; quedan en el historial) y actualizar `README.md` (versión actual, nº de páginas, fila nueva en el historial de cambios, próxima versión).
3. Commit y push a la rama de desarrollo de la sesión **y a `main`** (`git checkout main && git merge --ff-only <rama> && git push origin main`, luego volver a la rama).
4. Enviar los dos PDF al autor por el chat (herramienta SendUserFile, `display: attach`).
5. Si una corrección pertenece a un cambio recién hecho y el autor dice "en la misma versión", rehacer esa versión en vez de crear otra.
6. Antes de dar por bueno: renderizar las páginas tocadas con `pdftoppm` y mirarlas.

## Preferencias del autor
- Respuestas concretas, sin afirmar lo que no esté verificado; en español.
- Temas médicos con revisiones de 2022 en adelante; preguntar si quiere un PowerPoint del tema (por ahora ha dicho que no para el libro).
- Imágenes: tamaño mediano y nítidas; sin pie de foto/número salvo que lo pida. Si inserta contenido que no cabe, usar una página nueva **sin número impreso** para no alterar la numeración ni el índice.
- Pies de foto en versalitas "FIGURA n.m." con fuente del libro; en EN traducir.
- Decir con claridad lo que no pudo verificarse (p. ej. citas).

## Cómo se editan los PDF (no hay archivo fuente)
- Python con `pypdf` (`PdfWriter(clone_from=...)`, nunca actualización incremental) y `reportlab` para dibujar texto/figuras. Usar `python3 -I`.
- Cada página son «tiras» (formularios `fzFrmN`, ver `tools/strips3.py`) con una matriz de desplazamiento; se reubican cambiando matrices o reescribiendo el contenido de la página.
- Fuente del libro: TeX Gyre Pagella. Instalar `fonts-texgyre` (apt) y convertir con `tools/otf2ttf.py` (requiere `pip install fonttools`) para usarla en reportlab.
- Márgenes: texto en x 76–511 pt (páginas pares) y 84–519 pt (impares); cabecera en y≈787 desde abajo.
- `pdftotext` sobre el libro completo se cuelga: usar páginas sueltas (`-f N -l N`) con `timeout`.
- Scripts de referencia: `tools/capitulo17/` (capítulo completo: contenido, composición, figuras e integración) y `tools/ejemplos/` (inserciones de figuras, pies, apartados nuevos, figura vectorial). Son ejemplos con rutas del entorno anterior: hay que adaptarlos.
- Pendientes y notas de revisión: sección final de `README.md`.
