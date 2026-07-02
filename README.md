# Landing "Hoguera Santa en el Monte Sión"

Landing **estática** (HTML + CSS + JS, sin Node ni backend) para la campaña **Hoguera Santa
en el Monte Sión** de la Iglesia Universal del Reino de Dios.

Estilo cinematográfico oscuro con acentos dorados y tipografía serif. Incluye:

- Hero con versículo (Joel 2:32) y animación de entrada.
- Slider de **3 videos** (Historias reales).
- Slider de **versículos con efecto máquina de escribir** + **4 pestañas** ("¿Qué puedes esperar?").
- **Testimonios** con foto y efecto hover.
- **Compositor de peticiones**: el usuario escribe su petición, se dibuja sobre la hoja oficial
  del Monte Sión y se **descarga en PDF**.
- CTA al portal de voto de fe.

Se publica **dentro de WordPress** (`universal.org.mx`) pegando un bloque en el **widget HTML de
Elementor**.

---

## Estructura del repo

```
landing-hoguera-santa/
├── index.html                # La landing: aquí se EDITAN textos y estructura
├── assets/
│   ├── css/landing.css        # Estilos (tema cinematográfico / dorado)
│   └── img/
│       ├── hero/hero-monte-sion.png          # Imagen del hero
│       └── peticion/peticion-monte-sion.jpg  # Hoja de petición (para el canvas)
├── Dockerfile                 # Imagen nginx para previsualizar
├── docker-compose.yml         # Levanta la landing en http://localhost:8080
├── nginx/default.conf         # Config nginx del contenedor
├── docs/GITEA_BRANCH_PROTECTION.md  # Cómo proteger main (solo aneg mergea)
├── pegar-en-elementor.html   # Solo en rama `dev`: bloque listo para pegar en Elementor
└── README.md
```

> **¿Qué archivo edito?**
> - **Textos** → `index.html`
> - **Estilos / colores / espaciados** → `assets/css/landing.css`
> - **Imágenes** → `assets/img/...`
>
> El archivo `pegar-en-elementor.html` **NO se edita a mano**: es una copia para desplegar y vive
> únicamente en la rama `dev`.

---

## Repositorios

| Remote | URL | Uso |
|--------|-----|-----|
| **Gitea (principal)** | https://git.allanmontero.com/aneg/landing-hoguera-santa | Equipo + PRs a `main` |
| **GitHub** | https://github.com/AntoEstrada11/landing-hoguera-santa | Backup / jsDelivr CDN |

```bash
git remote add gitea https://git.allanmontero.com/aneg/landing-hoguera-santa.git
```

---

## Ramas y protección de `main`

| Rama | Para qué |
|------|----------|
| **`main`** | Producción. Solo merge vía **Pull Request** aprobado por **aneg**. |
| **`dev`** | Desarrollo. Incluye `pegar-en-elementor.html`. |
| **`contenido`** | Edición de textos para colaboradores no técnicos. |

**Flujo:** trabajo en `dev` (o `contenido`) → **PR a `main`** → **aneg aprueba y mergea**.

Configuración paso a paso en Gitea (hacer una vez):  
→ **[docs/GITEA_BRANCH_PROTECTION.md](docs/GITEA_BRANCH_PROTECTION.md)**

---

## Previsualizar localmente

### Opción A — Docker (recomendado)

Requisito: [Docker Desktop](https://www.docker.com/products/docker-desktop/) en ejecución.

```bash
docker compose up -d --build
```

Abrir **http://localhost:8080**

Comandos útiles:

```bash
docker compose logs -f landing-hoguera-santa   # ver logs
docker compose down                            # detener
docker compose up -d --build                   # rebuild tras cambios
```

### Opción B — Python (sin Docker)

```bash
python -m http.server 8000
# http://localhost:8000/index.html
```

> Usa siempre un servidor local (no `file://`): el compositor de peticiones dibuja sobre un
> `<canvas>` y `file://` puede bloquear la descarga.

---

## Publicar en WordPress (Elementor)

1. Edita la página con **Elementor**.
2. Crea una **Sección** en **Ancho completo** y con **padding 0**.
3. Dentro, agrega el widget **HTML** (o *HTML personalizado*).
4. Abre **`pegar-en-elementor.html`** (rama `dev`), copia **todo** y pégalo en el widget.
5. **Publica** y revisa en **Ver página** (no solo en el editor).

> **Optimizado para Elementor:** el bloque es **ligero** (~40 KB). El CSS completo
> (`landing-elementor.css`) se carga por JavaScript **solo en la página publicada**;
> en el editor solo hay una vista previa mínima para no congelar el panel.
>
> Regenerar tras cambios: `python scripts/gen-elementor.py`
>
> Si al publicar no ves estilos, purga caché jsDelivr:
> `https://purge.jsdelivr.net/gh/AntoEstrada11/landing-hoguera-santa@main/assets/css/landing-elementor.css`

---

## Contenido principal

- **Hero:** `assets/img/hero/hero-monte-sion.png` + versículo Joel 2:32.
- **Historias reales:** slider de 3 videos de YouTube (`GIeJ2iYUZaE`, `idEbXWmndj8`, `4q7WPFFpuJo`).
- **¿Qué puedes esperar?:** slider de versículos (autoplay 13 s, efecto máquina de escribir) y 4
  pestañas (Dirección espiritual · Apertura económica · Restauración familiar · Paz interior).
- **Testimonios:** foto circular + nombre, con zoom al pasar el mouse.
- **Voto / petición:** compositor sobre la hoja oficial con **descarga en PDF** y CTA a
  [primicias.iurdsys.net](https://primicias.iurdsys.net/).

---

Proyecto interno · Iglesia Universal del Reino de Dios — México.
