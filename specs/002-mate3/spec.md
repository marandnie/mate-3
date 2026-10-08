# Spec 002: Mate 3, carrusel de la materia

- **Estado:** draft implementado y verificado en local, pendiente de revisión (no publicado)
- **Fecha:** 2026-10-08
- **Repo:** [marandnie/mate-3](https://github.com/marandnie/mate-3), servido por GitHub Pages en https://mandieto.com.ar/mate-3/
- **Dueña:** Marina Nieto

## 1. Objetivo

Que `/mate-3/` sea el showcase de lo trabajado en **Matemática III** (Tecnicatura Universitaria en Programación Informática, UNSAM, 2.º cuatrimestre de 2021): un carrusel de diapositivas con los temas de cada clase, los parciales y el TP final.

Se mantiene el stack (Jekyll en GitHub Pages + reveal.js) y el estilo actual de diapositivas (tema *moon*: fondo azul oscuro, títulos en League Gothic), que a Marina le gusta por limpio y elegante.

## 2. Decisiones de Marina (2026-10-08)

| # | Tema | Decisión |
|---|------|----------|
| D1 | Stack | Mismo stack: Jekyll + reveal.js. Se mantiene el look de diapositivas. |
| D2 | Formato | Carrusel con los temas abordados en cada clase. |
| D3 | Fuente | La carpeta local de la materia (material de cada clase, parciales, TP) y el repo. |
| D4 | Publicación | Ver el draft antes de hacer push. |
| D5 | Nombre público | "Marina Nieto" (sin "Andrea"), igual que en el sitio principal. |
| D6 | Estilo de texto | Sin raya larga (—): se usa guion o dos puntos. |

## 3. Auditoría del estado actual (2026-10-08)

| Área | Hallazgo | Severidad |
|---|---|---|
| Contenido | Solo 3 diapositivas: portada, "Clase 1" con el texto `01-02` y "Clase 2" con `01-03` (placeholders). | Alta |
| Dependencia externa | `baseurl: "/slides"` hace que el CSS y el JS se carguen de `/slides/node_modules/reveal.js/` (otro repo, reveal.js 3.x). Si ese repo cambia, `/mate-3/` se rompe. El repo ya trae reveal.js **4.2.1** en `node-modules/reveal.js-master/` y no se usa. | Alta |
| Consola | 5 errores al cargar: `paper.css`, `marked.js`, `markdown.js`, `highlight.js` y `notes.js` dan 404 (rutas relativas a `/mate-3/node_modules/`, que no existe). | Media |
| Configuración | Las opciones `reveal:` de `_config.yml` no se usan: `script.html` inicializa reveal sin leerlas. | Baja |
| Metadatos | `<title>slides</title>`; descripción copiada de otro proyecto ("A fun activity for learning Git and GitHub."), y no se publica como meta description. Sin `lang`, canonical, favicon ni Open Graph. | Media |
| Páginas sobrantes | Se publican `demo.html`, `index.html`, `examples/` y `test/` de reveal.js, y el `README.md`. | Baja |
| Estructura | Las diapositivas son posts con fecha falsa (`0000-01-0N`). Para editar una clase hay que tocar un post y su orden depende del nombre del archivo. | Baja |

Material disponible (carpeta local "Mate 3"): 12 clases con fecha (06/08 a 29/10/2021), el 1.er parcial (clase 9, 01/10/2021), el 2.º parcial (12/11/2021) y su recuperatorio (19/11/2021), y el TP final (regresión lineal múltiple sobre viajes de Ecobici 2019).

## 4. Historias de usuaria

- **H1.** Como reclutadora o visitante, en un par de minutos entiendo qué se vio en la materia y qué hizo Marina con Python y datos.
- **H2.** Como visitante en el celular, paso las diapositivas con el dedo y las puedo leer sin hacer zoom.
- **H3.** Como Marina, para corregir o sumar una clase edito un único archivo de datos, sin tocar HTML.
- **H4.** Como visitante, puedo compartir el link a una clase puntual.
- **H5.** Como Google, entiendo de qué trata la página y que la autora es la misma persona que la del sitio principal.

## 5. Requisitos

### Contenido

- **R1.** Portada: Matemática III, TPI UNSAM, 2.º cuatrimestre 2021, Marina Nieto.
- **R2.** Mapa (índice) con acceso directo a cada clase, a los parciales y al TP.
- **R3.** Una diapositiva por clase (12): número, fecha, título, de 3 a 4 temas y un fragmento de código representativo.
- **R4.** Diapositivas de evaluación: 1.er parcial (en el lugar de la clase 9), 2.º parcial + recuperatorio, y TP final (planteo, método, resultados y conclusión).
- **R5.** Cierre con links al repo, a los notebooks y al sitio principal.
- **R6.** El código que sale de entregas de Marina (parciales, TP) se marca con su origen. El resto son ejemplos breves del tema.
- **R7.** Textos en castellano, sin raya larga, con el nombre "Marina Nieto" (D5, D6).

### Navegación

- **R8.** Carrusel horizontal: flechas visibles, teclado, swipe, barra de progreso y número de diapositiva (`actual/total`).
- **R9.** Cada diapositiva tiene URL propia (por ejemplo `/mate-3/#/clase-05`).
- **R10.** En pantallas verticales (celular) el contenido pasa a una columna y la tipografía queda legible.

### Técnica

- **R11.** Mismo stack (D1): Jekyll compatible con GitHub Pages + reveal.js, tema *moon*.
- **R12.** Autocontenido: reveal.js 4.2.1 desde el propio repo; ninguna referencia a `/slides/`.
- **R13.** El contenido de las clases vive en un único archivo de datos (`_data/clases.yml`).
- **R14.** La consola del navegador no muestra errores.
- **R15.** Metadatos: `lang="es-AR"`, `<title>` y meta description propios, canonical, Open Graph con imagen de 1200×675, favicon del sitio y JSON-LD que declare como autora a `https://mandieto.com.ar/#person` (la misma `Person` de la spec 001).
- **R16.** No se publican las demos ni los tests de reveal.js, ni el `README.md`.

### Fuera de este repo

- **R17.** La página Trabajos del sitio principal enlaza a `/mate-3/`.

## 6. Criterios de aceptación

Verificables con `specs/002-mate3/check.py` (contra el build local o contra el sitio publicado) y en el navegador:

- **CA1.** `index.html` tiene `<html lang="es-AR">`, un solo `<title>`, meta description de 50 a 170 caracteres y canonical `https://mandieto.com.ar/mate-3/`.
- **CA2.** Toda referencia local (`link`, `script`, `img`) existe en el build y ninguna apunta a `/slides/`.
- **CA3.** Hay 12 diapositivas de clase (`clase-01` a `clase-12`), cada una con fecha, título y al menos 3 temas. La 9 es el 1.er parcial.
- **CA4.** Todos los links del mapa apuntan a un `id` de diapositiva que existe.
- **CA5.** Todas las `<img>` tienen `alt`, `width` y `height`; los `<svg>` tienen `role="img"` y `aria-label`.
- **CA6.** El texto visible no contiene "—" ni "Andrea".
- **CA7.** La imagen `og:image` existe, mide 1200×675 y pesa menos de 200 KB.
- **CA8.** No existen en el build: `README.md`, `node-modules/reveal.js-master/{demo.html,index.html,examples/,test/}`.
- **CA9.** (Navegador) reveal.js inicializa, 0 errores de consola, la cantidad de diapositivas es la esperada y `#/clase-05` abre esa clase. Capturas a 1280×800 y 390×844 sin texto cortado ni desbordes.

## 7. Fuera de alcance

- Reorganizar o borrar el material de clase que ya está en el repo (PDF, videos, zips; ~480 MB).
- Renombrar los notebooks (sus nombres de archivo incluyen el nombre completo).
- Corregir el 1.er parcial o rehacer el TP: se muestran como se entregaron.

## 8. Preguntas abiertas

- **P1.** ¿Nombrar a la docente (Mónica Hencek) en la portada? En el draft: no.
- **P2.** Los notebooks enlazados tienen `Nieto_Marina_Andrea` en el nombre del archivo. ¿Renombrarlos (y actualizar links)? En el draft: se enlazan tal cual.
- **P3.** Las fechas salen de los nombres de las carpetas de cada clase (caen viernes); la agenda de la facultad dice jueves. ¿Se muestran igual? En el draft: sí.
- **P4.** El repo publica el material de la cátedra (PDF y videos) bajo `/mate-3/archivos de clase, pdfs/`. ¿Queda así?
