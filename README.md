# Sergio A. Mora Pardo — portfolio

Portafolio bilingüe (inglés/español) de Sergio A. Mora Pardo, enfocado en liderazgo técnico de AI/ML, sistemas de machine learning en producción, experimentación causal y docencia.

El diseño toma como referencia la estructura narrativa de Adritian para Hugo, con una implementación propia, ligera y sin dependencias de tema.

## Desarrollo local

Requiere Hugo `0.165.0` o posterior.

```bash
hugo server
```

El sitio queda disponible en `http://localhost:1313/` y se recarga al editar contenido, plantillas o estilos.

## Validación

```bash
hugo --gc --minify --cleanDestinationDir --destination /tmp/sergio-portfolio-build
python3 scripts/check_site.py /tmp/sergio-portfolio-build
```

El verificador revisa rutas internas, fragmentos, idioma del documento, jerarquía principal, texto alternativo, directivas de indexación y la integridad básica del PDF.

## Estructura

- `content/`: páginas y casos de estudio en ambos idiomas.
- `data/portfolio.yaml`: experiencia, métricas, capacidades, docencia y publicaciones.
- `layouts/`: plantillas Hugo y componentes compartidos.
- `assets/`: CSS y JavaScript procesados por Hugo Pipes.
- `static/`: retrato, tarjetas sociales, imágenes históricas y CV público.
- `.github/workflows/hugo.yaml`: compilación y despliegue en GitHub Pages.

## CV público

El documento se sirve en:

`https://sergiomorapardo.github.io/cv/sergio-mora-cv.pdf`

El archivo está excluido del rastreo en `robots.txt`, aunque cualquier persona con la URL puede abrirlo. Antes de publicar una nueva versión conviene revisar sus datos de contacto.

## Despliegue

Los cambios enviados a `master` activan el workflow de GitHub Pages. En la configuración del repositorio, la fuente de Pages debe estar establecida en **GitHub Actions**.
