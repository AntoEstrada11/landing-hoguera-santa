# Landing "Hoguera Santa en el Monte Sión"

Landing **autocontenida** para la campaña **Hoguera Santa en el Monte Sión** de la Iglesia
Universal del Reino de Dios. Estilo cinematográfico oscuro con acentos dorados, tipografía serif
(Cormorant Garamond), animaciones de aparición al hacer scroll, un slider de promesas
(video + versículo) y un **compositor de peticiones** que dibuja el texto del usuario sobre la
hoja oficial y permite descargarla.

Pensada para vivir **dentro de WordPress** (en `universal.org.mx`), incrustada mediante un
**`<iframe>`**. Es 100% estática: HTML + CSS + JS, sin Node ni backend.

---

## Estructura del repo

```
landing-hoguera-santa/
├── index.html              # Página demo (assets locales, ideal para desarrollo)
├── hoguera-embed.html      # ⭐ Página autocontenida para incrustar por <iframe> (producción)
├── elementor-embed.html    # Bloque HTML+CSS+JS inline (solo si se pega en un widget HTML con permisos)
├── peticion.html           # Hoja de petición imprimible (Monte Sión)
├── assets/
│   ├── css/landing.css      # Tema visual (cinematográfico/dorado) de la demo
│   └── img/
│       ├── hero/hero-monte-sion.png        # Imagen del hero
│       └── peticion/peticion-monte-sion.jpg # Hoja de petición (local, para el canvas)
└── README.md
```

> **¿Cuál archivo uso?**
> - **`hoguera-embed.html`** → es el entregable de producción. Se sube a un hosting y se incrusta con un `<iframe>`.
> - **`index.html`** → demo de desarrollo; usa los assets locales (`assets/...`).
> - **`elementor-embed.html`** → solo sirve si tienes permiso `unfiltered_html` para pegar `<style>`/`<script>` directo en un widget HTML. Si no, usa el iframe.

---

## Ramas y flujo de trabajo

Repositorio: **https://github.com/AntoEstrada11/landing-hoguera-santa**

| Rama | Propósito |
|------|-----------|
| **`main`** | Producción. Código estable y publicado. **No se hace push directo** (solo vía PR). |
| **`dev`** | Integración de desarrolladores. |
| **`contenido`** | Edición de textos / diseño (para los colaboradores no técnicos). |

**Flujo sugerido:**

1. **Diseñadores / edición de texto:** trabajan en `contenido` → abren **Pull Request a `dev`**.
2. **Desarrolladores:** integran en `dev` → cuando está listo, **Pull Request de `dev` a `main`** (producción).
3. `main` debería estar **protegida** (Settings → Branches): requiere PR y, opcionalmente, aprobaciones.

```bash
# Clonar
git clone https://github.com/AntoEstrada11/landing-hoguera-santa.git
cd landing-hoguera-santa

# Trabajar en contenido (textos)
git checkout contenido
# ...editar textos en index.html / hoguera-embed.html...
git add -A && git commit -m "Ajuste de textos sección X"
git push origin contenido
# luego abrir PR a dev en GitHub
```

---

## Previsualizar localmente

No hace falta Node. Con cualquier servidor estático:

```bash
# Python 3
python -m http.server 8765
# luego abre http://localhost:8765
```

- `http://localhost:8765/` → demo completa (`index.html`).
- `http://localhost:8765/hoguera-embed.html` → la página que se incrusta en producción.
- `http://localhost:8765/peticion.html` → hoja de petición.

> Usa siempre un servidor local (no `file://`): el compositor de peticiones dibuja una imagen en
> `<canvas>` y `file://` puede bloquear esa operación.

---

## Despliegue (incrustar en WordPress)

La página se publica como archivo y se incrusta con un `<iframe>`. Hay dos escenarios según
dónde se aloje `hoguera-embed.html`.

### Opción A — Mismo dominio que WordPress (recomendada)

Sube `hoguera-embed.html` al propio servidor de `universal.org.mx`
(p. ej. `wp-content/uploads/hoguera/`) por **cPanel / FTP / WP File Manager**:

```
https://universal.org.mx/wp-content/uploads/hoguera/hoguera-embed.html
```

Ventajas: el **alto del iframe se autoajusta** solo (script interno) y la **descarga de la
petición funciona** sin CORS (imagen en el mismo dominio).

Incrustar (widget HTML de Elementor, o shortcode de **Advanced iFrame** si no tienes permisos):

```html
<iframe
  src="https://universal.org.mx/wp-content/uploads/hoguera/hoguera-embed.html"
  title="Hoguera Santa en el Monte Sión"
  scrolling="no"
  style="display:block;width:100vw;max-width:100vw;margin-left:calc(50% - 50vw);border:0;height:100vh;overflow:hidden;">
</iframe>
```

O con Advanced iFrame:

```text
[advanced_iframe src="https://universal.org.mx/wp-content/uploads/hoguera/hoguera-embed.html" width="100%" height="3000" scrolling="no"]
```

### Opción B — Hosting externo (Netlify / GitHub Pages / Cloudflare)

Sube **toda la carpeta** (para que estén `assets/`) y apunta el iframe a esa URL externa.

⚠️ Al ser **otro dominio**:
- El alto **no** se autoajusta → usa un `height` fijo grande en el shortcode/iframe.
- La **descarga de la petición** falla a menos que la imagen de la hoja esté en el **mismo dominio**
  que la página. En ese caso, apunta la imagen de petición a la ruta local
  `assets/img/peticion/peticion-monte-sion.jpg` (mismo origen) en lugar de la URL de WordPress.

---

## Permisos en WordPress (importante)

Si tu usuario **no es administrador completo** (no ves "Usuarios"/"Plugins"/"Ajustes"), WordPress
**elimina** `<style>`, `<script>` e `<iframe>` pegados directamente en el contenido
(falta la capacidad `unfiltered_html`). Síntomas típicos: "se ve sin CSS", el widget **HTML** no
aparece en Elementor, o el editor se rompe.

**Solución:** incrustar por **iframe** (los shortcodes/iframe de plugins como *Advanced iFrame* no
se filtran) en vez de pegar el HTML completo. Por eso el entregable es `hoguera-embed.html` + iframe.

---

## Contenido y recursos

- **Hero:** imagen `assets/img/hero/hero-monte-sion.png` (en producción puede apuntar a la URL de
  WordPress). Versículo Joel 2:32 con tipografía serif dorada.
- **Historias reales:** testimonios con foto circular y nombre.
- **Slider "¿Qué puedes esperar?":** 3 diapositivas (video de YouTube + versículo), autoplay con
  flechas y puntos, pausa al interactuar. Videos: `GIeJ2iYUZaE`, `idEbXWmndj8`, `4q7WPFFpuJo`.
- **Compositor de peticiones:** el usuario escribe su petición y se dibuja sobre la hoja oficial;
  se puede descargar como imagen. Imagen base: `assets/img/peticion/peticion-monte-sion.jpg`.
- **CTA "voto de fe":** botón con `href="#"` — **reemplázalo** por la URL real del portal.

---

## Pendientes / TODO

- [ ] Poner la **URL real** del portal de voto/donación (botón `lp-voto-cta__btn`, hoy `href="#"`).
- [ ] Confirmar las URLs definitivas de las imágenes en producción.
- [ ] (Opcional) Limpiar archivos heredados que ya no se usan.

---

## Solución de problemas

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| "Se ve sin CSS" / sin estilos | Usuario sin `unfiltered_html`; se borró `<style>`/`<script>` | Incrustar por **iframe**, no pegar el HTML |
| El editor de Elementor no abre tras pegar | Bloque enorme pegado en el widget corrompe los datos | Pegar solo el `<iframe>` pequeño |
| Texto invisible en algunas secciones | El script de animación no corrió | Ya hay *failsafe*; si persiste, incrustar por iframe (los scripts corren dentro) |
| El iframe sale muy angosto | El tema lo mete en un contenedor | El embed ya hace *full-bleed*; o pon la sección en "Ancho completo" |
| El alto del iframe no se ajusta | Está en otro dominio (cross-origin) | Aloja en el **mismo dominio** o usa `height` fijo |
| La descarga de la petición falla | Imagen de petición en otro dominio (canvas "tainted") | Usa la imagen local (mismo origen que la página) |

---

Proyecto interno · Iglesia Universal del Reino de Dios — México.
