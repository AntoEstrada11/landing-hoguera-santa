"""Genera pegar-en-elementor.html (ligero) + assets/css/landing-elementor.css (scoped)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CDN = "https://cdn.jsdelivr.net/gh/AntoEstrada11/landing-hoguera-santa@main"
CSS_URL = f"{CDN}/assets/css/landing-elementor.css"

SCOPED_GLOBALS = """
.landing,
.landing *,
.landing *::before,
.landing *::after {
  box-sizing: border-box;
}

.landing {
  width: 100vw;
  max-width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  overflow-x: hidden;
  scroll-behavior: smooth;
  font-family: var(--lp-font);
  color: var(--lp-text-on-light);
  background: var(--lp-ink);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

.landing .container {
  width: 100%;
  max-width: var(--lp-max);
  margin: 0 auto;
  padding: 0 clamp(1.25rem, 4vw, 2rem);
}

.landing a {
  color: inherit;
  transition: color 0.2s var(--lp-ease);
}

.landing a:focus-visible,
.landing button:focus-visible,
.landing summary:focus-visible,
.landing input:focus-visible,
.landing select:focus-visible,
.landing textarea:focus-visible {
  outline: 2px solid var(--lp-accent);
  outline-offset: 2px;
}
"""

# Vista mínima en el editor de Elementor (evita congelar el panel).
EDITOR_PREVIEW_CSS = """
.landing {
  width: 100vw;
  max-width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  background: #160a05;
  color: #fff;
  font-family: system-ui, sans-serif;
  line-height: 1.5;
  overflow-x: hidden;
}
.landing .container { max-width: 75rem; margin: 0 auto; padding: 0 1.25rem; }
.landing .lp-section-head,
.landing .lp-promesas,
.landing .lp-testimonial,
.landing .lp-flow__item,
.landing .lp-faq__item,
.landing .lp-peticion,
.landing .lp-versiculo { opacity: 1 !important; transform: none !important; }
.landing .lp-versiculo { position: relative; opacity: 1; }
.landing .lp-versiculo:not(:first-child) { margin-top: 1rem; }
"""

SCRIPT_BOOTSTRAP = """<script>
(function () {
  'use strict';

  var CSS_URL = '__CSS_URL__';
  var landing = document.querySelector('.landing');
  if (!landing) return;

  function isElementorEditor() {
    try {
      if (document.body && document.body.classList.contains('elementor-editor-active')) return true;
      if (/elementor-preview|action=elementor/i.test(window.location.href)) return true;
      if (window.elementorFrontend && typeof window.elementorFrontend.isEditMode === 'function' && window.elementorFrontend.isEditMode()) return true;
    } catch (e) { /* noop */ }
    return false;
  }

  if (isElementorEditor()) return;

  function injectCSS(done) {
    if (document.getElementById('lp-hoguera-css')) {
      if (done) done();
      return;
    }
    var link = document.createElement('link');
    link.id = 'lp-hoguera-css';
    link.rel = 'stylesheet';
    link.href = CSS_URL;
    link.onload = function () { if (done) done(); };
    link.onerror = function () { if (done) done(); };
    document.head.appendChild(link);
  }

  function boot() {
__INIT_BODY__
  }

  function start() {
    injectCSS(boot);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
</script>"""


def minify_css(css: str) -> str:
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", css)
    return css.strip()


def scope_css(raw: str) -> str:
    raw = re.sub(r"@import\s+url\([^)]+\)\s*;\s*", "", raw, count=1)
    m = re.search(r":root\s*\{[^}]*\}", raw, re.DOTALL)
    if not m:
        raise ValueError(":root block not found")
    root_block = m.group(0)

    marker = "/* —— Typography —— */"
    idx = raw.find(marker)
    if idx == -1:
        raise ValueError("Typography marker not found")

    return "\n".join([
        "@import url('https://fonts.googleapis.com/css2?family=Encode+Sans+Semi+Expanded:wght@400;500;600;700&display=swap');",
        "",
        root_block,
        SCOPED_GLOBALS.strip(),
        "",
        raw[idx:],
    ])


def extract_main_and_init(index_html: str) -> tuple[str, str]:
    main_m = re.search(r"<main class=\"landing\">.*?</main>", index_html, re.DOTALL)
    script_m = re.search(
        r"<script>\s*\(function \(\) \{\s*(.*?)\s*\}\)\(\);\s*</script>",
        index_html,
        re.DOTALL,
    )
    if not main_m or not script_m:
        raise ValueError("Could not extract main or script from index.html")
    return main_m.group(0), script_m.group(1)


def adapt_for_cdn(main: str, init: str, css: str) -> tuple[str, str, str]:
    hero_cdn = f"{CDN}/assets/img/hero/hero-monte-sion.png"
    peticion_cdn = f"{CDN}/assets/img/peticion/peticion-monte-sion.jpg"

    main = main.replace(
        'src="assets/img/hero/hero-monte-sion.png"',
        f'src="{hero_cdn}"',
    )
    init = init.replace(
        "img.src = 'assets/img/peticion/peticion-monte-sion.jpg';",
        (
            "img.crossOrigin = 'anonymous';\n"
            f"      img.src = '{peticion_cdn}';"
        ),
    )
    css = css.replace(
        "url('../img/hero/hero-monte-sion.png')",
        f"url('{hero_cdn}')",
    )
    return main, init, css


def build_pegar_html(main: str, init: str) -> str:
  # Indent init body for inside boot()
    init_indented = "\n".join(
        ("    " + line if line.strip() else line) for line in init.splitlines()
    )

    script = SCRIPT_BOOTSTRAP.replace("__CSS_URL__", CSS_URL).replace(
        "__INIT_BODY__", init_indented
    )

    header = f"""<!-- ============================================================
     HOGUERA SANTA EN EL MONTE SIÓN — Bloque para Elementor
     ------------------------------------------------------------
     Pega TODO este archivo en un widget HTML (sección ancho completo, padding 0).

     Optimizado para Elementor:
     - Sin <!DOCTYPE>, <html>, <head> ni <body> (rompen el editor).
     - CSS completo se carga por JS solo en la página publicada (no en el editor).
     - Scripts desactivados en el editor para evitar congelamiento.
     - Vista previa mínima en el panel de edición.

     Tras publicar, si no ves estilos, purga caché jsDelivr:
     https://purge.jsdelivr.net/gh/AntoEstrada11/landing-hoguera-santa@main/assets/css/landing-elementor.css
     ============================================================ -->

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Encode+Sans+Semi+Expanded:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&display=swap" rel="stylesheet">
<style id="lp-hoguera-editor-preview">{EDITOR_PREVIEW_CSS.strip()}</style>

"""

    return header + main + "\n\n" + script + "\n"


def main() -> None:
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    css_raw = (ROOT / "assets/css/landing.css").read_text(encoding="utf-8")
    main, init = extract_main_and_init(index)
    main, init, css_raw = adapt_for_cdn(main, init, css_raw)

    scoped_css = scope_css(css_raw)
    elementor_css_path = ROOT / "assets/css/landing-elementor.css"
    elementor_css_path.write_text(scoped_css, encoding="utf-8", newline="\n")

    pegar = build_pegar_html(main, init)
    pegar_path = ROOT / "pegar-en-elementor.html"
    pegar_path.write_text(pegar, encoding="utf-8", newline="\n")

    print(f"OK: {elementor_css_path.name} ({len(scoped_css):,} chars)")
    print(f"OK: {pegar_path.name} ({len(pegar):,} chars, ligero para Elementor)")


if __name__ == "__main__":
    main()
