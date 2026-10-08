# Plan técnico: Spec 002, carrusel de Mate 3

## Restricciones de la plataforma

- El repo `mate-3` es un sitio de proyecto de GitHub Pages: se sirve en `https://mandieto.com.ar/mate-3/` porque el sitio principal tiene el dominio propio. Por eso `baseurl: "/mate-3"`.
- GitHub Pages construye con **Jekyll 3.10** en modo `safe`. No hace falta ningún plugin: todo es Liquid + HTML.
- En Jekyll 3, `exclude:` **reemplaza** la lista por defecto, así que se repite completa.
- reveal.js ya está en el repo: `node-modules/reveal.js-master/` (4.2.1, con guion, no guion bajo: por eso Jekyll lo publica). Se usa `dist/` y `plugin/` y se excluye el resto.
- Las rutas de favicon apuntan al sitio principal (`https://mandieto.com.ar/favicon.*`): es el mismo dominio.

## Diseño

### Contenido en un solo archivo → `_data/clases.yml` (R13)

Una lista en el orden del carrusel. Cada elemento:

```yaml
- id: clase-05            # ancla: /mate-3/#/clase-05
  numero: 5               # para la etiqueta "Clase 05"
  fecha: 03/09/2021
  titulo: Funciones
  mapa: Funciones         # texto de la baldosa en el mapa (sin `mapa` no aparece)
  temas: [ ... ]          # 3 a 4 viñetas
  codigo:
    origen: Del 1.er parcial   # opcional: marca el código propio (R6)
    texto: |
      def ...
  include: parcial-1.html # opcional: diapositiva especial con HTML propio
```

Las clases comunes usan la plantilla `_includes/slides/clase.html`. Las evaluaciones (1.er parcial, 2.º parcial, TP) tienen `include:` porque llevan imágenes o gráficos.

### Página → `index.html` + `_layouts/presentation.html`

```
.reveal
├── a.volver            ← link fijo a mandieto.com.ar
└── .slides
    ├── portada         (fijo)
    ├── mapa            (baldosas generadas desde clases.yml)
    ├── for item in site.data.clases
    │     include: slides/<item.include> o slides/clase.html
    └── cierre          (fijo)
```

Se eliminan `_posts/`, `_layouts/slide.html`, `_layouts/print.html` e `_includes/slide.html` (el esquema de posts con fecha `0000-01-0N`).

### Diapositivas de detalle → pilas verticales (R18, R19)

reveal.js arma una pila vertical cuando una `<section>` contiene otras `<section>`: la primera es la principal y las demás quedan "abajo" (flecha hacia abajo, tecla ↓, swipe hacia arriba). En `clases.yml`, un elemento con `detalle:` genera la pila:

```yaml
- id: tp-final
  ...
  detalle:
    - id: tp-datos
      titulo: Preparación de los datos
      bajada: texto corto arriba          # opcional
      temas: [ ... ]                      # opcional
      tabla: { columnas: [...], filas: [[...], ...] }   # opcional
      cifras: [ { valor: "18,98", texto: "minutos de error" } ]  # opcional
      barras: { unidad: min, filas: [ { texto: ..., valor: 48.2 } ] }  # opcional
      codigo: { origen: Del TP final, texto: ... }       # opcional
      salida: |                           # opcional: salida impresa del notebook
        ...
    - id: tp-resultados
      include: tp-resultados.html         # para lo que lleva imágenes
```

```
section                      ← pila (sin id)
├── section#tp-final         ← principal: link "Más detalle ↓" al pie
├── section#tp-datos         ← plantilla genérica slides/detalle.html
├── section#tp-modelo
├── section#tp-resultados    ← include propio (boxplots)
└── section#tp-simulaciones
```

- Plantilla genérica `_includes/slides/detalle.html`: a la izquierda bajada, temas, tabla, cifras o barras; a la derecha código y salida. Sin código ni salida, ocupa todo el ancho.
- La etiqueta de cada detalle repite la del padre y suma la posición (`2 / 5`).
- Las barras de las simulaciones del TP son `div` con ancho proporcional al valor (una sola escala, con el valor escrito al lado).
- La salida de los notebooks se muestra en un bloque aparte con la clase `nohighlight` (sin colores de sintaxis).
- En el mapa, la baldosa de una pila muestra cuántas diapositivas de detalle tiene.

| Pila | Detalle | Fuente |
|---|---|---|
| 1.er parcial | La consigna: estructuras de datos y preguntas | Notebook del parcial |
| Clase 12 | Las 5 etapas del análisis, aplicadas al TP | PDF de la clase 12 + TP |
| 2.º parcial | El grafo en números; regex de aeropuertos y precios | Notebook del recuperatorio (salidas impresas) |
| TP final | Preparación de datos; modelo y error; resultados; simulaciones y conclusión | Notebook del TP (código y salidas) |

### `<head>` → `_includes/head.html` (R12, R15)

- `lang="es-AR"`, `<title>`, meta description, canonical, Open Graph y Twitter card desde `_config.yml`.
- CSS: `dist/reset.css`, `dist/reveal.css`, `dist/theme/moon.css`, `plugin/highlight/monokai.css` y `assets/css/mate3.css`. Todo con `relative_url`.
- Favicon del sitio principal.
- JSON-LD: `WebPage` con `author` y `Person` con `@id` `https://mandieto.com.ar/#person` (el mismo de la spec 001) e `isPartOf` → `https://mandieto.com.ar/#website`.

### Script → `_includes/script.html` (R8 a R10, R14)

- `dist/reveal.js` + `plugin/highlight/highlight.js`. Se sacan markdown y notes (no se usan; hoy dan 404).
- Opciones desde `site.reveal | jsonify` (`hash`, `controls`, `progress`, `slideNumber: "c/t"`, transición).
- **Modo vertical:** si la ventana es más alta que ancha, se agrega la clase `vertical` al `<html>` y reveal usa un lienzo de 540×1170 en vez de 1200×760. Al rotar el teléfono se reconfigura con `Reveal.configure`. El CSS pasa las columnas a una sola.

### Estilo → `assets/css/mate3.css` (R11)

Sobre el tema *moon* (colores Solarized). Sin tocar el CSS de reveal:

- Etiqueta de la clase (`Clase 05 · 03/09/2021`) en amarillo Solarized (`#b58900`), títulos en League Gothic.
- Grilla de dos columnas: temas a la izquierda, código a la derecha.
- Bloques de código sobre `#073642` con la paleta monokai y una pestaña que dice "Ejemplo" o el origen (R6).
- Mapa: 7×2 baldosas (2 columnas en vertical); las evaluaciones con borde amarillo.
- Imágenes de notebooks sobre tarjetas claras (son PNG de fondo blanco).

### Figuras

| Diapositiva | Figura | Fuente |
|---|---|---|
| 1.er parcial | Diagrama de Venn | Salida original del notebook del parcial (PNG). |
| 2.º parcial | Grafo ponderado de 8 nodos con el camino de Dijkstra A → H resaltado | SVG dibujado a partir de la lista de aristas y de los resultados impresos en el notebook del recuperatorio. El PNG original pone los pesos en aristas equivocadas (las etiquetas usan un `pos` distinto al del dibujo), así que se redibuja en vez de reutilizarlo. |
| TP final | Boxplots de duración por franja horaria y por misma estación | Salidas originales del notebook del TP (PNG). Se deja afuera el boxplot por género: el 99 % de los viajes tiene género "NO INFORMADO" (76.369 de 77.136). |
| Open Graph | Portada a 1200×675 | Captura del build local, JPEG < 200 KB. |

El código de las entregas (parciales y TP) se muestra tal como se entregó; solo se cortan algunas líneas largas para que entren en la diapositiva y en el celular.

### Configuración → `_config.yml`

- `title`, `description`, `url: https://mandieto.com.ar`, `baseurl: /mate-3`, `lang`, `author`, `timezone: America/Argentina/Buenos_Aires`.
- `reveal:` con las opciones que de verdad se pasan a `Reveal.initialize`.
- `exclude:` la lista por defecto + `README.md`, `LICENSE`, `specs/`, `package-lock.json` y, dentro de reveal.js, `css/`, `js/`, `examples/`, `test/`, `demo.html`, `index.html`, `gulpfile.js`, `package*.json`, `README.md` (R16).

### Sitio principal (R17)

`trabajos.md` suma una línea con link a `/mate-3/`. Va en una rama aparte del repo `marandnie.github.io`.

## Verificación

- Build local con la gema `github-pages` (Jekyll 3.10.0) y `--safe`, con `--baseurl /mate-3`.
- `specs/002-mate3/check.py` (solo biblioteca estándar) valida CA1 a CA8 contra `_site/` o contra el sitio publicado:

```bash
python3 specs/002-mate3/check.py _site                         # build local
python3 specs/002-mate3/check.py https://mandieto.com.ar/mate-3  # producción
```

- CA9 con Chromium (Playwright): errores de consola, `Reveal.getTotalSlides()`, navegación por hash y capturas a 1280×800 y 390×844.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Se rompe el link a la página vieja `/slides/...` | Nadie enlaza a esas rutas desde `/mate-3/`; el repo `slides` sigue igual. |
| El build de Pages tarda por los ~480 MB de material | Ya pasa hoy; no se suma peso (las imágenes nuevas pesan < 300 KB en total). |
| El modo vertical deja texto chico en pantallas muy angostas | Lienzo propio de 640 px de ancho y una sola columna; se verifica a 390 px. |
| Código del 2.º parcial con detalles mejorables (`super().__init__(self)`) | Se muestra tal como se entregó (fuera de alcance corregirlo). |
