# Mate 3

Lo que trabajé en **Matemática III** (Tecnicatura Universitaria en Programación Informática, UNSAM, 2.º cuatrimestre 2021): Python, NumPy, Pandas, grafos con NetworkX, expresiones regulares y regresión lineal.

- Carrusel con los temas de cada clase: https://mandieto.com.ar/mate-3/
- TP final (regresión lineal múltiple sobre viajes de Ecobici 2019): [`Tp_final_mate3_Nieto_Marina_Andrea.ipynb`](Tp_final_mate3_Nieto_Marina_Andrea.ipynb)
- Parciales: [`archivos de clase, pdfs/Parciales/`](archivos%20de%20clase%2C%20pdfs/Parciales/)

## Cómo está hecho

Jekyll (GitHub Pages) + [reveal.js](https://revealjs.com/) 4.2.1, que está en `node-modules/reveal.js-master/`.

- El contenido de cada clase está en `_data/clases.yml`. Para corregir o sumar una clase, se edita ese archivo.
- Las diapositivas con imágenes o gráficos (parciales y TP) están en `_includes/slides/`.
- Estilos propios sobre el tema *moon*: `assets/css/mate3.css`.
- Spec, plan y tareas: `specs/002-mate3/`.

Para verlo en local:

```bash
bundle install
bundle exec jekyll serve --baseurl /mate-3
# http://localhost:4000/mate-3/
python3 specs/002-mate3/check.py _site
```
