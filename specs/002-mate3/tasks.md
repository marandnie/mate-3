# Tareas: Spec 002, carrusel de Mate 3

`[x]` hecho · `[ ]` pendiente · `(Rn)` requisito · `(CAn)` criterio de aceptación

## Fase 1: Base

- [x] T01 `_config.yml`: título, descripción, `url`, `baseurl: /mate-3`, `lang`, opciones de reveal y `exclude`. (R12, R15, R16)
- [x] T02 Borrar el esquema viejo: `_posts/`, `_layouts/slide.html`, `_layouts/print.html`, `_includes/slide.html`.
- [x] T03 `_layouts/presentation.html` + `_includes/head.html` (metadatos, CSS de reveal 4.2.1 local, favicon, JSON-LD). (R11, R12, R15, CA1, CA2)
- [x] T04 `_includes/script.html`: reveal + highlight, opciones desde `_config.yml`, modo vertical. (R8, R9, R10, R14)

## Fase 2: Contenido

- [x] T05 `_data/clases.yml` con las 12 clases, el 2.º parcial y el TP. (R3, R4, R6, R7, R13, CA3)
- [x] T06 Plantillas: `slides/clase.html`, portada y mapa en `index.html`, cierre. (R1, R2, R5, CA4)
- [x] T07 Diapositivas especiales: `parcial-1.html`, `parcial-2.html` (grafo SVG), `tp-planteo.html`, `tp-resultados.html`. (R4, R6, CA5)
- [x] T08 Imágenes: salidas de los notebooks (Venn, 2 boxplots) en `assets/img/`. (CA5)
- [x] T09 `assets/css/mate3.css`: grilla, etiquetas, código, mapa, tarjetas, modo vertical. (R10, R11)

## Fase 3: Verificación

- [x] T10 `specs/002-mate3/check.py` (CA1 a CA8).
- [x] T11 Build local (Jekyll 3.10.0, `--safe`) + `check.py _site` en verde.
- [x] T12 Navegador: consola sin errores, total de diapositivas, `#/clase-05`, capturas a 1280×800 y 390×844. (CA9)
- [x] T13 Imagen Open Graph 1200×675 < 200 KB desde la portada. (R15, CA7)

### Resultado de la verificación (2026-10-08)

| Contra | Resultado |
|---|---|
| Sitio publicado hoy (antes de los cambios) | 3 diapositivas placeholder; 5 errores de consola; CSS y JS desde `/slides/` |
| Build local de esta rama (Jekyll 3.10.0, `--safe`, gema `github-pages` 232) | `check.py _site`: **Todo OK** (CA1 a CA8) |
| Chromium a 1280×800, 1920×1080, 390×844 y 844×390 | 18 diapositivas, 0 errores de consola, `#/clase-05` abre la clase 5, las baldosas del mapa navegan, nada se sale del lienzo (CA9) |

## Fase 4: Revisión del draft 1 (2026-10-08)

- [x] T14 Revisar el draft y responder P1 a P4 de la spec. → D7 a D11.
- [x] T19 Spec, plan y tareas con las decisiones D7 a D11, R18, R19 y CA10.
- [x] T20 `clases.yml`: `detalle:` en clase 9, clase 12, 2.º parcial y TP (el TP pasa de 2 diapositivas horizontales a una pila de 5). (R18)
- [x] T21 `_includes/slides/detalle.html` (bajada, temas, tabla, cifras, barras, código, salida) + pilas en `index.html`. (R18)
- [x] T22 Link "Más detalle ↓", posición en la etiqueta y marca en el mapa. (R19, CA10)
- [x] T23 Docente en la portada. (R1, D8)
- [x] T24 `check.py`: pilas (CA10). Build + navegador (CA9) en desktop y celular.

### Resultado de la verificación del draft 2 (2026-10-08)

| Contra | Resultado |
|---|---|
| Build local (Jekyll 3.10.0, `--safe`) | `check.py _site`: **Todo OK** (CA1 a CA8 y CA10): 4 pilas, 25 diapositivas |
| Chromium a 1280×800 y 390×844 | 0 errores de consola; nada se sale del lienzo; `#/tp-modelo` abre la pila del TP en el 3.er lugar; "Más detalle", la flecha ↓ y "Ver el TP final" navegan bien (CA9) |

## Fase 5: Publicación (Marina)

- [ ] T15 Push de la rama `mate3/002-carrusel` a `marandnie/mate-3` y merge a `main`.
- [ ] T16 Después del deploy: `python3 specs/002-mate3/check.py https://mandieto.com.ar/mate-3` y mirar la página en el celular.
- [ ] T17 Sitio principal: link a `/mate-3/` en Trabajos (rama aparte en `marandnie.github.io`). (R17)
- [ ] T18 Search Console: inspeccionar `https://mandieto.com.ar/mate-3/` y pedir indexación.
