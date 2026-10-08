#!/usr/bin/env python3
"""Chequeos de aceptación de la spec 002 (carrusel de Mate 3).

Uso:
    python3 specs/002-mate3/check.py _site                           # build local
    python3 specs/002-mate3/check.py https://mandieto.com.ar/mate-3  # sitio publicado

Valida CA1 a CA8. CA9 (consola, navegación y capturas) se verifica en el navegador.
Solo usa la biblioteca estándar. Sale con código 1 si algún chequeo falla.
"""
import argparse
import json
import os
import re
import struct
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

CANONICAL = "https://mandieto.com.ar/mate-3/"
BASEURL = "/mate-3"
CLASES = [f"clase-{n:02d}" for n in range(1, 13)]
PROHIBIDO_EN_TEXTO = ["\u2014", "Andrea"]  # raya larga (D6) y nombre completo (D5)
NO_PUBLICAR = [  # CA8
    "/README.md",
    "/node-modules/reveal.js-master/demo.html",
    "/node-modules/reveal.js-master/index.html",
    "/node-modules/reveal.js-master/examples/backgrounds.html",
    "/node-modules/reveal.js-master/test/test-auto-animate.html",
]


class Pagina(HTMLParser):
    """Junta lo necesario de index.html: metadatos, referencias, diapositivas y texto visible."""

    VOID = {"meta", "link", "img", "br", "hr", "input", "source", "area", "base", "col", "embed", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.titles = []
        self.meta = {}
        self.links = []
        self.scripts = []
        self.imgs = []
        self.svgs = []
        self.anchors = []
        self.sections = []  # dicts: id, class, texto
        self.jsonld = []
        self.texto = []
        self._pila = []
        self._buf = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key.lower()] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
        elif tag == "script":
            if a.get("src"):
                self.scripts.append(a["src"])
            if a.get("type") == "application/ld+json":
                self._buf = []
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "svg":
            self.svgs.append(a)
        elif tag == "a":
            self.anchors.append(a)
        elif tag == "section":
            self.sections.append({"id": a.get("id"), "class": a.get("class", ""), "texto": []})
        elif tag == "title" and not self._en("svg"):
            self._buf = []
        if tag not in self.VOID:
            self._pila.append(tag)

    def handle_endtag(self, tag):
        if tag == "title" and self._buf is not None and not self._en("svg"):
            self.titles.append("".join(self._buf).strip())
            self._buf = None
        elif tag == "script" and self._buf is not None:
            self.jsonld.append("".join(self._buf))
            self._buf = None
        if tag in self._pila:
            while self._pila and self._pila.pop() != tag:
                pass

    def handle_data(self, data):
        if self._buf is not None:
            self._buf.append(data)
            return
        if self._en("script") or self._en("style") or self._en("head"):
            return
        self.texto.append(data)
        if self._en("section") and self.sections:
            self.sections[-1]["texto"].append(data)

    def _en(self, tag):
        return tag in self._pila


class Fuente:
    """Lee archivos del build local o URLs del sitio publicado."""

    def __init__(self, target):
        self.remoto = target.startswith("http")
        self.target = target.rstrip("/")

    def get(self, ruta):
        """Devuelve (status, bytes) para una ruta del sitio, relativa a /mate-3/ (p. ej. '/assets/x.png')."""
        if self.remoto:
            url = self.target + urllib.parse.quote(ruta, safe="/%")
            req = urllib.request.Request(url, headers={"User-Agent": "mate3-check/1.0"})
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    return r.status, r.read()
            except urllib.error.HTTPError as e:
                return e.code, b""
        rel = urllib.parse.unquote(ruta).lstrip("/")
        if rel == "" or rel.endswith("/"):
            rel += "index.html"
        f = os.path.join(self.target, rel)
        if not os.path.isfile(f):
            return 404, b""
        with open(f, "rb") as fh:
            return 200, fh.read()


def tamano_imagen(data):
    """(ancho, alto) de un JPEG o PNG."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


class Reporte:
    def __init__(self):
        self.fallas = 0

    def check(self, codigo, ok, msg):
        print(f"  [{'OK' if ok else 'FALLA'}] {codigo} {msg}")
        if not ok:
            self.fallas += 1


def ruta_local(ref):
    """Convierte una referencia del HTML a ruta relativa a /mate-3/, o None si es externa."""
    p = urllib.parse.urlparse(ref)
    if p.scheme or p.netloc or ref.startswith("#"):
        return None
    ruta = p.path
    if ruta.startswith(BASEURL + "/"):
        return ruta[len(BASEURL):]
    return ruta  # relativa o fuera de /mate-3/: se reporta igual


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="carpeta _site o URL de la página (https://mandieto.com.ar/mate-3)")
    args = ap.parse_args()

    src = Fuente(args.target)
    rep = Reporte()

    status, body = src.get("/")
    if status != 200:
        sys.exit(f"No se pudo leer index.html ({status})")
    p = Pagina()
    p.feed(body.decode("utf-8"))

    print("CA1 metadatos")
    desc = p.meta.get("description", "")
    canon = [l.get("href") for l in p.links if "canonical" in (l.get("rel") or "").split()]
    rep.check("CA1", p.lang == "es-AR", f'<html lang="{p.lang}">')
    rep.check("CA1", len(p.titles) == 1, f"un <title>: {p.titles}")
    rep.check("CA1", 50 <= len(desc) <= 170, f"description de {len(desc)} caracteres")
    rep.check("CA1", canon == [CANONICAL], f"canonical {canon}")
    try:
        grafo = json.loads(p.jsonld[0])["@graph"]
        autor = next(n for n in grafo if n.get("@type") == "WebPage")["author"]["@id"]
        rep.check("CA1", len(p.jsonld) == 1 and autor == "https://mandieto.com.ar/#person",
                  f"JSON-LD con autora {autor}")
    except (IndexError, KeyError, ValueError, StopIteration) as e:
        rep.check("CA1", False, f"JSON-LD inválido: {e}")

    print("\nCA2 referencias locales")
    refs = [l.get("href") for l in p.links if "stylesheet" in (l.get("rel") or "").split()]
    refs += p.scripts + [i.get("src") for i in p.imgs]
    for ref in refs:
        rep.check("CA2", "/slides/" not in ref, f"no usa /slides/: {ref}")
        ruta = ruta_local(ref)
        if ruta is None:
            continue
        st, _ = src.get(ruta)
        rep.check("CA2", st == 200, f"{ref} responde {st}")

    print("\nCA3 diapositivas de clase")
    ids = [s["id"] for s in p.sections]
    rep.check("CA3", len(ids) == len(set(ids)) and None not in ids, f"{len(ids)} diapositivas, todas con id único")
    for cid in CLASES:
        s = next((s for s in p.sections if s["id"] == cid), None)
        if s is None:
            rep.check("CA3", False, f"falta #{cid}")
            continue
        texto = " ".join("".join(s["texto"]).split())
        tiene_fecha = re.search(r"\d{2}/\d{2}/\d{4}", texto) is not None
        st = body.decode("utf-8")
        bloque = st[st.find(f'id="{cid}"'):]
        bloque = bloque[:bloque.find("</section>")]
        temas = len(re.findall(r"<li>", bloque[bloque.find('class="temas'):]))
        rep.check("CA3", tiene_fecha and "<h2>" in bloque and temas >= 3,
                  f"#{cid}: fecha {'sí' if tiene_fecha else 'no'}, {temas} temas")
    s9 = next((s for s in p.sections if s["id"] == "clase-09"), {"texto": []})
    rep.check("CA3", "parcial" in "".join(s9["texto"]).lower(), "#clase-09 es el 1.er parcial")

    print("\nCA4 mapa")
    for a in p.anchors:
        href = a.get("href", "")
        if href.startswith("#/"):
            rep.check("CA4", href[2:] in ids, f"{href}")

    print("\nCA5 imágenes accesibles")
    for img in p.imgs:
        ok = bool(img.get("alt", "").strip()) and img.get("width") and img.get("height")
        rep.check("CA5", ok, f"{img.get('src')}: alt, width y height")
    for svg in p.svgs:
        ok = svg.get("role") == "img" and bool(svg.get("aria-label", "").strip())
        rep.check("CA5", ok, f"<svg class=\"{svg.get('class')}\">: role=img y aria-label")

    print("\nCA6 texto visible")
    visible = "".join(p.texto) + " ".join(i.get("alt", "") for i in p.imgs)
    for palabra in PROHIBIDO_EN_TEXTO:
        n = visible.count(palabra)
        rep.check("CA6", n == 0, f"{palabra!r} aparece {n} veces")

    print("\nCA7 imagen para redes")
    og = p.meta.get("og:image", "")
    ruta = urllib.parse.urlparse(og).path
    ruta = ruta[len(BASEURL):] if ruta.startswith(BASEURL) else ruta
    st, img = src.get(ruta)
    dims = tamano_imagen(img) if st == 200 else None
    rep.check("CA7", st == 200 and dims == (1200, 675) and len(img) < 200_000,
              f"{og}: {st}, {dims}, {len(img) // 1024} KB")

    print("\nCA8 archivos que no se publican")
    for ruta in NO_PUBLICAR:
        st, _ = src.get(ruta)
        rep.check("CA8", st == 404, f"{ruta} responde {st}")

    print()
    if rep.fallas:
        print(f"{rep.fallas} falla(s)")
        sys.exit(1)
    print("Todo OK")


if __name__ == "__main__":
    main()
