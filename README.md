# Landing "Hoguera Santa en el Monte Sión"

Landing y **bloque embebible autocontenido** para la campaña **Hoguera Santa en el Monte Sión**
de la Iglesia Universal del Reino de Dios. Reutiliza el diseño de la landing de fidelidad/diezmo,
pero con el contenido, paleta (fuego) y enlaces de Hoguera Santa.

Pensado para insertarse **dentro de WordPress + Elementor** (solo acceso a `wp-admin`, sin Node,
sin FTP/SSH). El entregable principal es un bloque **HTML + CSS + JS** que se pega en un widget
"HTML personalizado" de Elementor. **No requiere servidor Node/Nitro.**

---

## Contenido del repo

```
landing-hoguera-santa/
├── index.html              # Página demo completa (hero + secciones + bloque interactivo)
├── peticion.html           # Hoja de petición imprimible (Monte Sión)
├── widget/
│   └── index.html          # ⭐ Bloque embebible AUTOCONTENIDO (esto se pega en Elementor)
├── assets/
│   └── css/landing.css     # Tema visual (fuego) para la página demo
├── data/
│   └── iglesias.json       # Catálogo de iglesias (respaldo, ya embebido en el widget)
├── elementor-hoguera-localizador.json  # Plantilla Elementor importable (opcional)
└── README.md
```

> El **widget** (`widget/index.html`) es 100% autocontenido: trae su CSS y su JS en línea y
> carga Leaflet por CDN. El catálogo de iglesias va **embebido** dentro del propio widget como
> respaldo, así que funciona aunque la API externa no responda.

---

## Previsualizar localmente

No hace falta Node. Con cualquier servidor estático:

```bash
# Python 3
python -m http.server 8765
# luego abre http://localhost:8765
```

- `http://localhost:8765/` → landing demo completa.
- `http://localhost:8765/widget/index.html` → solo el bloque embebible.
- `http://localhost:8765/peticion.html` → hoja de petición.

> Abrir los archivos con `file://` (doble clic) puede bloquear la geolocalización y algunas
> peticiones (CORS). Usa siempre un servidor local para probar el mapa.

---

## Cómo pegar el bloque en Elementor

### Opción A — Pegar el HTML manualmente (recomendada)

1. Abre **`widget/index.html`** y edita el objeto **`HS_CONFIG`** (ver tabla abajo) con tus URLs
   reales (portal de pago, hoja de petición, API de iglesias…).
2. Copia **todo** lo que está entre los comentarios:

   ```html
   <!-- HS:WIDGET-START -->
   ...
   <!-- HS:WIDGET-END -->
   ```

3. En Elementor: arrastra un widget **"HTML"** (HTML personalizado) a la sección donde quieras
   el localizador y **pega** ahí el contenido.
4. Publica y prueba en el front-end (no solo en el editor).

> ⚠️ **Prueba que el widget HTML de Elementor permita `<script>`.** Algunos temas o plugins de
> seguridad lo filtran. Si el mapa no carga, revisa la consola del navegador y la sección
> "Solución de problemas".

### Opción B — Importar plantilla

1. En WordPress: **Plantillas → Plantillas guardadas → Importar plantillas**.
2. Sube `elementor-hoguera-localizador.json`.
3. Inserta la plantilla en tu página y edita el `HS_CONFIG` dentro del widget HTML.

---

## Configuración del widget (`HS_CONFIG`)

Al inicio del `<script>` del widget hay un objeto editable:

| Clave | Qué es | Ejemplo |
|-------|--------|---------|
| `iglesiasApiUrl` | URL de la API de iglesias (formato bloques). Vacío = usa solo el catálogo embebido. | `https://tu-api.com/api/elementos` |
| `iglesiasApiKey` | **No la pongas en producción** (queda expuesta). Autoriza por CORS/origen. | `''` |
| `portalUrl` | Enlace al portal de pago / voto de fe ya existente. **Reemplázalo.** | `https://www.mercadopago.com.mx/...` |
| `peticionUrl` | URL de la hoja de petición. En WP usa la URL absoluta del archivo subido. | `https://tusitio.com/peticion.html` |
| `telefono` / `telefonoHref` | Teléfono visible y para `tel:` | `55 55 74 32 66` / `+525555743266` |
| `nominatimBase` | Servicio de geocodificación (Nominatim público). | (por defecto) |
| `osrmBase` | Servicio de rutas (OSRM público). | (por defecto) |

> El botón **"Hacer mi voto de fe"** es **solo un enlace** a tu portal de pago existente.
> Aquí **no se integra ninguna pasarela de pago**.

---

## Imágenes y videos

- **Hero:** la demo ya usa un **slider con las 3 imágenes oficiales** de la campaña
  (`/wp-content/uploads/2026/06/1.png`, `2.png`, `3.png`). Para cambiarlas, edita los `<img>`
  dentro de `.lp-hero__media` en `index.html`.
- **Sin barra de navegación:** la página no incluye menú propio (se inserta dentro de
  `universal.org.mx`, que ya tiene el suyo).
- **Testimonios en video:** la sección "Historias reales" embebe los videos oficiales de YouTube
  con carga diferida (solo cargan al hacer clic, para no penalizar la velocidad):
  `GIeJ2iYUZaE`, `idEbXWmndj8`, `4q7WPFFpuJo`.
- **Hoja de petición oficial (imagen):**
  `https://universal.org.mx/wp-content/uploads/2026/06/PETICION-MONTE-SION_l.jpg`
  Puedes enlazarla directamente o usar `peticion.html` de este repo (rellena nombre, iglesia y
  fecha automáticamente desde la URL).

---

## El localizador de iglesias + mapa

- **Buscador** por nombre / ciudad / dirección sobre el catálogo.
- **"Usar mi ubicación"**: geolocaliza al usuario, hace *reverse geocode* (Nominatim) y muestra
  las Universal cercanas por coincidencia de zona.
- **Mapa Leaflet** (CDN) con marcador del usuario y de la iglesia, **ruta** a pie / auto (OSRM)
  y botones a **Google Maps / Waze**.
- **Descargar mi petición**: abre `peticion.html` con el nombre de la iglesia precargado.
- **Hacer mi voto de fe**: enlaza a tu portal de pago.

### Fuentes de datos externas (sin servidor propio)

| Servicio | Uso | Nota |
|----------|-----|------|
| API de iglesias | Catálogo en vivo | Debe **habilitar CORS** para `universal.org.mx` |
| Nominatim (OSM) | Geocodificación / reverse | Límite de uso público (~1 req/seg) |
| OSRM (project-osrm) | Cálculo de rutas | Servicio público de demostración |

---

## ⚠️ Consideraciones importantes (documentadas)

1. **CORS de la API de iglesias.** Como el navegador llama directo a la API, esta debe responder
   con `Access-Control-Allow-Origin` para tu dominio (`https://universal.org.mx`). Si no, el widget
   usará automáticamente el **catálogo embebido** de respaldo.
2. **API key.** No incrustes la API key en el navegador (cualquiera la ve). Autoriza la API
   **por origen/CORS**. `iglesiasApiKey` solo para pruebas.
3. **Coordenadas precargadas.** El catálogo embebido trae los nombres pero **no** coordenadas.
   El widget geocodifica **solo la iglesia seleccionada** (1 petición a Nominatim por selección)
   para respetar los límites de uso. **Ideal:** que la API entregue `lat`/`lng` por iglesia
   (el widget ya los usa si vienen). Formato admitido por iglesia:
   ```json
   { "nombre": "CENTRO - QUERETARO", "direccion": "...", "lat": 20.59, "lng": -100.39 }
   ```
   Con coordenadas, el mapa muestra distancias y marcadores sin geocodificar.
4. **Nominatim / OSRM públicos** tienen límites de uso. Para producción de alto tráfico,
   conviene un servicio propio o coordenadas precargadas (ver punto 3).
5. **`<script>` en Elementor.** Verifica que el widget HTML permita scripts; algunos plugins de
   seguridad los eliminan.

---

## Qué se quitó respecto a la landing de diezmo

- Toda la lógica de **pago** (Mercado Pago): gate, checkout, composables, endpoints, `/pago/resultado`.
- El **wizard** que pedía nombre/apellido/teléfono y "Continuar al pago".
- La **analítica server-side** (`events.jsonl`). Para medir, usa Google Analytics del WordPress.
- Toda dependencia de **endpoints `/api/*` propios (Nitro)**. Ahora todo es estático.

## Qué se conservó / adaptó

- Diseño y secciones: hero, enseñanza, beneficios, testimonios, FAQ (con contenido Hoguera).
- Localizador de iglesias + mapa, ahora **autocontenido** (Leaflet por CDN, sin servidor propio).
- Hoja de petición adaptada al **Monte Sión**.
- Botón CTA **"Hacer mi voto de fe"** como enlace al portal existente.

---

## Solución de problemas

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| El mapa no aparece | El tema/plugin filtró `<script>` o el CDN está bloqueado | Permite scripts en el widget HTML; revisa consola |
| "No pudimos acceder a tu ubicación" | El sitio no está en HTTPS o se negó el permiso | La geolocalización exige HTTPS; acepta el permiso |
| La búsqueda funciona pero no hay distancias | La API no entrega coordenadas | Carga `lat`/`lng` en el catálogo (ver consideración 3) |
| No carga el catálogo en vivo | Falta CORS en la API | Usa el respaldo embebido o habilita CORS |

---

Proyecto interno · Iglesia Universal del Reino de Dios — México.
