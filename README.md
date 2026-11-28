# Anestesia y Obesidad — ES / EN

Última versión en español del libro *Anestesia y obesidad* y su equivalente en inglés (*Anesthesia and Obesity*). Todos los cambios se hacen **en ambos libros**.

**Versión de trabajo actual: v41**

- `Anestesia_y_Obesidad_ES_v41.pdf` (277 páginas)
- `Anesthesia_and_Obesity_EN_v41.pdf` (276 páginas)

> **Chat nuevo:** leer primero `CLAUDE.md` (flujo obligatorio y notas técnicas). La versión de trabajo es la indicada arriba; cada cambio crea la siguiente versión y actualiza este repositorio (rama de trabajo y `main`).

## Reglas de trabajo (acordadas con el autor)

1. Cada cambio genera una **nueva versión** numerada en orden ascendente (próxima: **v42**), en español e inglés.
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
| v28 | **Capítulo 17 nuevo**: «Cuidados posanestésicos, criterios de alta y tromboprofilaxis en el paciente con obesidad» (14 páginas, ES y EN; ES págs. 225–238, EN págs. 223–236). Unifica el material de Vera Health y OpenEvidence sin repetir información: criterios de alta de la URPA, consideraciones ventilatorias/cardiovasculares/quirúrgicas, alta el mismo día, tromboprofilaxis (dosis de enoxaparina por IMC), trombosis portomesentérica, caso clínico, puntos clave y 35 referencias. Incluye 2 figuras redibujadas (17.1 monitorización respiratoria tras cirugía bariátrica; 17.2 algoritmo de trombosis esplácnica) y 4 tablas. Se actualizó el índice general; Siglas/Abbreviations renumeradas. |
| v38 | **Capítulo 14 (TIVA)**: (1) imagen 1 (taller «TIVA con TCI») al final de los objetivos de aprendizaje, antes de 14.1 (ES pág. 175; EN pág. 174); el apartado 14.1 pasó a una página nueva sin número, junto con las líneas finales del párrafo que venían de la página siguiente, y 14.2 empieza ahora en la parte superior de la siguiente. (2) imagen 2 (tablet de cálculo TCI) tras el texto de 14.4.1 (ES pág. 180; EN pág. 178), en una página nueva sin número; el párrafo «La tabla 14.4 muestra…» pasó a esa página bajo la imagen (en EN lo acompaña la tabla 14.4, que estaba en el mismo párrafo). Sin pie de foto ni número. ES 274 págs., EN 273 págs.; la numeración impresa no cambia. Scripts en `tools/v38/`. |
| v39 | Imagen «Paciente pediátrico obeso con SAOS: manejo anestésico TIVA y vía aérea» en el capítulo 15, tras «Monitorización mínima» de 15.7 (ES pág. 206; EN pág. 205), sin pie de foto ni número. En ES ocupa una página nueva sin número entre las págs. 206 y 207 (15.8 sigue empezando en la 207); en EN la página nueva sin número lleva la imagen y, debajo, el título 15.8 con el texto que le seguía en esa página. ES 275 págs., EN 274 págs. Script: `tools/v38/build_v39.py`. |
| v40 | Infografía del capítulo 10 (objetivos, consideraciones en la obesidad, monitorización, estrategia y tipos de líquidos) bajo el cuadro de objetivos de aprendizaje, antes de 10.1 (ES pág. 137; EN pág. 136), sin pie de foto ni número. El apartado 10.1 pasó a una página nueva sin número (la figura 10.1 sigue en la página siguiente). La imagen está en español también en el libro en inglés. ES 276 págs., EN 275 págs. Script: `tools/v38/build_v40.py`. |
| v41 | Capítulo 6: (1) ecografía abdominal (FAST) en 6.10, bajo «…si la sospecha persiste» y antes de «Trombosis venosa profunda» (ES pág. 97; EN pág. 96); el resto de la página bajó. (2) Foto del abordaje del neuroeje en paciente obeso bajo el título 6.14 (ES págs. 98–99; EN págs. 97–98): 6.14 y su párrafo inicial pasaron a una página nueva sin número, con la foto entre el título y el párrafo; 6.14.1 empieza ahora arriba de la página siguiente. Sin pie de foto ni número. ES 277 págs., EN 276 págs. Script: `tools/v38/build_v41.py`. |

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
| v29 | Figura 8.5 nueva (3 fotos de intubación despierta con fibrobroncoscopio) tras el apartado 8.5.2, con pie «Secuencia de intubación despierta con fibrobroncoscopio en paciente obeso con vía aérea difícil». La figura 8.4 y el texto posterior se desplazaron; se añadió una página sin número (ES pág. 124; EN tras la 122). No se actualizó la lista de figuras del índice. |
| v30 | Imagen «Ecografía pulmonar: Seashore Sign vs. Código de Barras» (sin número ni pie de foto) al final del apartado 6.5.2 Neumotórax (ES pág. 94; EN pág. 93). Quedó en una página nueva sin número, con los apartados 6.5.3 y 6.6 desplazados a ella. |
| v31 | Sección 6.8 (ES pág. 96; EN pág. 95): dos fotos de punción de la arteria radial bajo el apartado «Línea arterial radial»; y en una página nueva sin número, cuadrícula 2×2 que relaciona las fotos de acceso venoso central con la imagen de ecografía correspondiente (fila 1: foto izquierda + ecografía 1; fila 2: foto derecha + ecografía 2). Sin pie de foto ni número. |
| v32 | El apartado «Acceso venoso central» (6.8) pasó a la página nueva sin número, encima de la cuadrícula 2×2 de imágenes, y se añadió bajo la cuadrícula el pie de imagen (sin número): «Acceso venoso central de la vena yugular interna del lado derecho en paciente obeso bajo guía ecográfica fuera de plano, con transductor lineal de alta frecuencia.» (traducido en EN). Se fusionó aquí la antigua v33 por indicación del autor. |
| v33 | Cuadrícula de 4 imágenes de la página 97: las dos de la fila inferior tienen el mismo tamaño y alineación que las de la fila superior (recortadas ligeramente para igualar proporciones). |
| v34 | Nuevo apartado **3.4.4** «Predicción integral de la vía aérea difícil en el paciente obeso…» tras 3.4.3 (ES/EN, págs. 39–40): imagen-resumen enviada por el autor (recortada la franja negra), texto del resumen, tabla 3.4 de evidencia 2022-2026 y conclusión. Ocupa 3 páginas nuevas sin número; el inicio de 3.5 pasó a la última. Sin referencias numeradas; verificar las citas de Bhargava 2023 y la revisión EJAIC 2023 (no se encontraron en una búsqueda rápida; Senoglu 2025, Madrid-Vázquez 2024 y Nair 2025 sí existen). El texto de la imagen está en español también en el libro en inglés. |
| v35 | El apartado de predicción integral de la vía aérea difícil se trasladó de 3.4.4 (págs. 39–40, que vuelven a su estado original) a **3.9.1**, tras la tabla 3.7 y antes de 3.10 (págs. 46–47). La tabla de evidencia pasó a ser la Tabla 3.8. En EN la tabla 3.7 estaba desplazada tras el primer punto de 3.10; se reordenó para que 3.10 quede después de 3.9.1. Tres páginas nuevas sin número en EN, dos en ES. |
| v36 | Figura 3.3 redibujada en vectores con la fuente del libro (TeX Gyre Pagella, estilo LaTeX), letras más grandes y nítidas (render a 3600×1680 px); contenido y texto sin cambios (ES y EN). |
| v37 | **Figura 10.2 eliminada** (línea arterial radial y monitorización del gasto cardíaco; ES pág. 172, EN pág. 171): imagen y pie de foto fuera, texto del capítulo 10 subido en la página y referencia «(figura 10.2)» suprimida del apartado 10.4. No se renumeró la figura 10.3 (queda como 10.3, sin 10.2). |

## Capítulo 17 — notas para revisión (v28)

- Las figuras 17.1 y 17.2 **se redibujaron** (en español e inglés) a partir de las capturas enviadas, con la atribución «Adaptado de…»; no se incrustaron las capturas originales por derechos de autor de las publicaciones. La 17.1 se atribuyó a Chand y Prathanvanich (J Intensive Care Med 2016) por coincidir con el texto de OpenEvidence; confirmar.
- El caso clínico (17.10) es **ilustrativo**, redactado para este capítulo; revisar.
- Umbral de caída de hemoglobina en alta el mismo día: el texto fuente daba «1,0 mmol/L» y «3,2 g/dL»; se mantuvo tal cual con las dos citas. Verificar en las fuentes originales.
- Las cifras de Zhang et al. 2026 (169 pacientes; OR 14,77/3,92/3,12) vienen de Vera Health y no se pudieron contrastar; el DOI y la cita sí se verificaron en Crossref.
- No se agregaron las siglas nuevas (HBPM, ACOD, TPM…) a la página de Siglas; se definen en el texto. Las listas de figuras y tablas del índice no se actualizaron (no cubren los capítulos recientes).
- El capítulo se compone con ReportLab (`ch17/` en el entorno de trabajo, no en el repositorio); el libro no tiene archivo fuente.
