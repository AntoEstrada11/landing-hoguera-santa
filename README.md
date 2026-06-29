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

## Ramas

Repositorio: **https://github.com/AntoEstrada11/landing-hoguera-santa**

| Rama | Para qué |
|------|----------|
| **`main`** | Producción. Solo lo editable (`index.html`, `assets/`, `README.md`). Limpia, para que edición identifique fácil qué tocar. |
| **`dev`** | Desarrollo. Incluye además `pegar-en-elementor.html` (bloque de despliegue). |
| **`contenido`** | Edición de textos para colaboradores no técnicos. |

**Flujo:** edición/desarrollo en `dev` (o `contenido`) → al estar listo, se lleva a `main`.

---

## Previsualizar localmente

No hace falta Node. Con cualquier servidor estático:

```bash
python -m http.server 8000
# luego abre: http://localhost:8000/index.html
```

> Usa siempre un servidor local (no `file://`): el compositor de peticiones dibuja sobre un
> `<canvas>` y `file://` puede bloquear la descarga.

---

## Publicar en WordPress (Elementor)

1. Edita la página con **Elementor**.
2. Crea una **Sección** en **Ancho completo** y con **padding 0**.
3. Dentro, agrega el widget **HTML** (o *HTML personalizado*).
4. Abre **`pegar-en-elementor.html`** (rama `dev`), copia **todo** y pégalo en el widget.
5. **Publica**.

Ese bloque carga el **CSS, el JS y las imágenes** desde el propio repo a través del CDN
**jsDelivr**, así no tienes que subir nada más a WordPress.

> **Caché del CDN:** con `@main`, jsDelivr puede tardar hasta ~12 h en reflejar cambios nuevos.
> Para forzar la actualización del CSS visita una vez:
> `https://purge.jsdelivr.net/gh/AntoEstrada11/landing-hoguera-santa@main/assets/css/landing.css`
> (o cambia `@main` por un commit/tag fijo para congelar la versión).
>
> **Requiere repo público** para que jsDelivr pueda servir los archivos. Si se vuelve privado,
> habría que subir CSS/JS/imágenes a la Biblioteca de Medios de WordPress.

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
