# Spec 002: Mate 3, carrusel de la materia

- **Estado:** draft 2 (con diapositivas de detalle), verificado en local, pendiente de revisión (no publicado)
- **Fecha:** 2026-10-08 (revisión 2 el mismo día)
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
| D7 | Profundidad (revisión del draft 1) | Las diapositivas que necesitan más profundidad tienen una flecha hacia abajo a diapositivas de detalle. |
| D8 | Docente (P1) | Se nombra a la docente, Mónica Hencek, en la portada. |
| D9 | Notebooks (P2) | Se enlazan tal cual, sin renombrar. |
| D10 | Fechas (P3) | Se mantienen las de las carpetas de cada clase. Coinciden con las de los propios parciales ("Clase 9, 1-10-2021"); la agenda de 2021 que decía jueves no cambia nada. |
| D11 | Material de la cátedra (P4) | Queda publicado en el repo como está. |

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

- **R1.** Portada: Matemática III, TPI UNSAM, 2.º cuatrimestre 2021, Marina Nieto y la docente, Mónica Hencek (D8).
- **R2.** Mapa (índice) con acceso directo a cada clase, a los parciales y al TP.
- **R3.** Una diapositiva por clase (12): número, fecha, título, de 3 a 4 temas y un fragmento de código representativo.
- **R4.** Diapositivas de evaluación: 1.er parcial (en el lugar de la clase 9), 2.º parcial + recuperatorio, y TP final (planteo, método, resultados y conclusión).
- **R5.** Cierre con links al repo, a los notebooks y al sitio principal.
- **R6.** El código que sale de entregas de Marina (parciales, TP) se marca con su origen. El resto son ejemplos breves del tema.
- **R7.** Textos en castellano, sin raya larga, con el nombre "Marina Nieto" (D5, D6).
- **R18.** Diapositivas de detalle (D7), en pilas verticales de reveal.js debajo de la diapositiva principal:
  - 1.er parcial: la consigna.
  - Clase 12: las 5 etapas del análisis de datos, aplicadas al TP.
  - 2.º parcial: el grafo en números (todas las operaciones del recuperatorio con su resultado) y el ejercicio de regex.
  - TP final: preparación de los datos, modelo y error, resultados, y simulaciones con la conclusión.
  - El contenido de detalle sale de los notebooks y del material de la materia; no se inventan resultados.

### Navegación

- **R8.** Carrusel horizontal: flechas visibles, teclado, swipe, barra de progreso y número de diapositiva (`actual/total`).
- **R9.** Cada diapositiva tiene URL propia (por ejemplo `/mate-3/#/clase-05`).
- **R10.** En pantallas verticales (celular) el contenido pasa a una columna y la tipografía queda legible.
- **R19.** Las diapositivas con detalle lo anuncian: link "Más detalle" al pie, flecha hacia abajo de reveal.js y una marca en su baldosa del mapa. Cada diapositiva de detalle muestra en qué posición de la pila está.

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
- **CA10.** Cada pila vertical tiene una diapositiva principal y al menos una de detalle, todas con `id`; el link "Más detalle" y la marca del mapa apuntan a diapositivas que existen.

## 7. Fuera de alcance

- Reorganizar o borrar el material de clase que ya está en el repo (PDF, videos, zips; ~480 MB).
- Renombrar los notebooks (D9).
- Corregir el 1.er parcial o rehacer el TP: se muestran como se entregaron.

## 8. Preguntas abiertas

Ninguna. P1 a P4 del draft 1 quedaron resueltas en D8 a D11.
