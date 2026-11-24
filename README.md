# Anestesia y Obesidad — ES / EN

Última versión en español del libro *Anestesia y obesidad* y su equivalente en inglés (*Anesthesia and Obesity*). Todos los cambios se hacen **en ambos libros**.

**Versión de trabajo actual: v27**

- `Anestesia_y_Obesidad_ES_v27.pdf` (253 páginas)
- `Anesthesia_and_Obesity_EN_v27.pdf` (252 páginas)

## Reglas de trabajo (acordadas con el autor)

1. Cada cambio genera una **nueva versión** numerada en orden ascendente (próxima: **v28**), en español e inglés.
2. Se trabaja siempre sobre la **última versión**.
3. Al crear una versión nueva se guarda en el repositorio, se **eliminan los archivos de la versión anterior** (quedan en el historial de git) y se envía al autor por el chat para descargar.
4. Nombres de archivo: `Anestesia_y_Obesidad_ES_vNN.pdf` y `Anesthesia_and_Obesity_EN_vNN.pdf`.
5. Los cambios en imágenes y pies de foto se aplican igual en los dos idiomas (leyendas traducidas al inglés).
6. Respuestas concretas, sin afirmar lo que no esté verificado; temas médicos con revisiones de 2022 en adelante; preguntar siempre si se desea un PowerPoint del tema.

## Historial de cambios (sesión del 23–24 nov. 2026)

| Versión | Cambio |
|---|---|
| v22 | Figura 6.7: imágenes A (foto con transductor convexo) y B (captura completa del ecógrafo, excursión diafragmática 30,81 mm), con letras A/B. |
| v23 | Figura 6.8: nueva imagen de ecografía pulmonar (pulmón normal, consolidación y líneas B, atelectasia con derrame), a ancho de texto en página propia, con nueva leyenda. Figura 6.10: nueva imagen de vena cava inferior en modo M (`vena cava modo M.JPG`) con pie de foto sobre índice de variabilidad y colapsabilidad de la VCI para evaluar volemia y carga de líquidos (mediciones 2,42 / 1,85 / 2,48 cm). |
| v24 | Dos imágenes sin número ni pie de foto: (1) fotos de quirófano al final de 6.8 Accesos vasculares ecoguiados, antes del título 6.9; (2) ilustración de pared abdominal bajo el título 6.9.1 Bloqueos de pared abdominal. |
| v25 | Figura 6.7 trasladada a la página 95, después de «…vigilancia respiratoria (figura 6.7B)» y antes de 6.7 FoCUS. |
| v26 | Pie de foto de la figura 6.12: paciente en **posición sentada** (no decúbito lateral). |
| v27 | Imagen del paciente con el equipo en quirófano bajo el título del capítulo 8, antes de «Objetivos de aprendizaje». |

## Pendientes / observaciones para las próximas versiones

- La imagen de la figura 6.8 tiene errores de texto en español (en ambos libros): «cuando a sospective atelectasis» y «Escana a supine paciente scama con obesidad». Pendiente decidir si se corrige o se rehace.
- Las dos imágenes añadidas en la v24 no tienen número ni pie de foto; el autor puede pedir leyendas (con o sin numeración).
- La figura 6.7 quedó después de la 6.8 en el orden del libro; se puede renumerar si se desea.
- La figura 6.10 original (canalización venosa periférica) fue reemplazada por la de vena cava inferior; la sección 6.8 no cita figura propia.
- El texto de la sección 6.14 menciona la posición del paciente; revisar coherencia con la figura 6.12 (posición sentada).

## Notas técnicas (cómo se editan estos PDF)

- Los PDF no tienen archivo fuente (LaTeX/Word); se editan directamente con `pypdf` (Python) y se revisan renderizando con `pdftoppm`.
- Cada página está compuesta por «tiras» (formularios `fzFrmN`) con matriz de desplazamiento; texto e imágenes se reubican modificando esas matrices o añadiendo contenido.
- Para insertar contenido que no cabe se añade una página nueva **sin número impreso** (así el índice y la numeración no cambian) y se traslada texto a ella.
- Se escribe siempre una copia completa (`PdfWriter(clone_from=...)`), no una actualización incremental: las incrementales dejaron páginas sin `/Parent`.
- Fuente de los pies de foto nuevos: TeX Gyre Pagella (la misma del libro), tamaño ≈ 9,9 pt; etiqueta «FIGURA» en versalitas.
- Los PDF son pesados; `pdftotext` sobre el documento completo se cuelga: usar páginas individuales (`-f N -l N`).
- Las páginas con figuras usan márgenes distintos en páginas pares (texto x 76–511) e impares (x 84–519).
