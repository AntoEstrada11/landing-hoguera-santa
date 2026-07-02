"""Genera pegar-en-elementor.html con CSS inline (Elementor no conserva <link> externos)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CDN = "https://cdn.jsdelivr.net/gh/AntoEstrada11/landing-hoguera-santa@main"

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


def scope_css(raw: str) -> str:
    raw = re.sub(
        r"@import\s+url\([^)]+\)\s*;\s*",
        "",
        raw,
        count=1,
    )
    m = re.search(r":root\s*\{[^}]*\}", raw, re.DOTALL)
    if not m:
        raise ValueError(":root block not found")
    root_block = m.group(0)

    marker = "/* —— Typography —— */"
    idx = raw.find(marker)
    if idx == -1:
        raise ValueError("Typography marker not found")
    component_css = raw[idx:]

    font_import = ""

    return "\n".join([
        root_block,
        SCOPED_GLOBALS.strip(),
        "",
        component_css,
    ])


def extract_main_and_script(index_html: str) -> tuple[str, str]:
    main_m = re.search(r"<main class=\"landing\">.*?</main>", index_html, re.DOTALL)
    script_m = re.search(
        r"<script>\s*\(function \(\) \{.*?\}\)\(\);\s*</script>",
        index_html,
        re.DOTALL,
    )
    if not main_m or not script_m:
        raise ValueError("Could not extract main or script from index.html")
    return main_m.group(0), script_m.group(0)


def adapt_for_cdn(main: str, script: str) -> tuple[str, str]:
    main = main.replace(
        'src="assets/img/hero/hero-monte-sion.png"',
        f'src="{CDN}/assets/img/hero/hero-monte-sion.png"',
    )
    script = script.replace(
        "img.src = 'assets/img/peticion/peticion-monte-sion.jpg';",
        (
            "img.crossOrigin = 'anonymous';\n"
            f"      img.src = '{CDN}/assets/img/peticion/peticion-monte-sion.jpg';"
        ),
    )
    return main, script


def build() -> str:
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets/css/landing.css").read_text(encoding="utf-8")
    main, script = extract_main_and_script(index)
    main, script = adapt_for_cdn(main, script)
    scoped = scope_css(css)

    header = """<!-- ============================================================
     HOGUERA SANTA EN EL MONTE SIÓN — Bloque para Elementor
     ------------------------------------------------------------
     CÓMO USARLO:
     1) En Elementor agrega un widget "HTML" (o "HTML personalizado").
        Tip: Sección a ANCHO COMPLETO y padding 0.
     2) Copia TODO este archivo y pégalo en el widget.
     3) Publica.

     NOTA: El CSS va INLINE (Elementor elimina los <link> externos).
     Si el editor se pone lento al pegar, guarda y previsualiza en
     "Ver página" — en el sitio publicado los estilos sí cargan.
     ============================================================ -->

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Encode+Sans+Semi+Expanded:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&display=swap" rel="stylesheet">
<style>
"""

    return header + scoped + "\n</style>\n\n" + main + "\n\n" + script + "\n"


def main() -> None:
    out = build()
    dest = ROOT / "pegar-en-elementor.html"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"OK: {dest.name} ({len(out):,} chars, CSS inline)")


if __name__ == "__main__":
    main()
