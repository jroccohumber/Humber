from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLIDES_DIR = ROOT / "slides"
ASSETS_DIR = ROOT / "assets"
WIDTH = 1600
HEIGHT = 900

COLORS = {
    "orange": "#F5A623",
    "orange_dark": "#E19112",
    "orange_soft": "#FFF2D8",
    "orange_mist": "#FFE2B0",
    "dark": "#231F20",
    "graphite": "#3A3336",
    "ink": "#4D474A",
    "cream": "#FCF8F1",
    "white": "#FFFFFF",
    "muted": "#7E767B",
    "line": "#EADFCF",
    "success": "#2EAF7D",
}


def esc(value: str) -> str:
    return escape(str(value), quote=True)


def text_block(
    x: int,
    y: int,
    lines: list[str],
    *,
    size: int = 24,
    line_height: int = 34,
    fill: str | None = None,
    weight: int = 400,
    anchor: str = "start",
    letter_spacing: float = 0,
    opacity: float | None = None,
) -> str:
    attrs = [
        f'x="{x}"',
        f'y="{y}"',
        f'font-size="{size}"',
        f'font-weight="{weight}"',
        f'fill="{fill or COLORS["dark"]}"',
        f'text-anchor="{anchor}"',
        'font-family="Arial, Helvetica, sans-serif"',
    ]
    if letter_spacing:
        attrs.append(f'letter-spacing="{letter_spacing}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')

    spans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        spans.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    return f"<text {' '.join(attrs)}>{''.join(spans)}</text>"


def chip(x: int, y: int, label: str, *, fill: str, text_fill: str, stroke: str | None = None) -> str:
    width = max(170, 24 + len(label) * 8)
    stroke_markup = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
    return (
        f'<g transform="translate({x} {y})">'
        f'<rect width="{width}" height="42" rx="21" fill="{fill}"{stroke_markup} />'
        f'{text_block(22, 27, [label], size=17, line_height=20, fill=text_fill, weight=700)}'
        "</g>"
    )


def panel(
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
    lines: list[str],
    *,
    dark: bool = False,
    accent: str | None = None,
    eyebrow: str | None = None,
) -> str:
    background = COLORS["dark"] if dark else COLORS["white"]
    title_fill = COLORS["white"] if dark else COLORS["dark"]
    body_fill = "#F5EEE6" if dark else COLORS["ink"]
    accent = accent or COLORS["orange"]
    eyebrow_fill = COLORS["orange_mist"] if dark else accent
    divider = "#4A4246" if dark else COLORS["line"]

    fragments = [
        f'<g transform="translate({x} {y})" filter="url(#card-shadow)">',
        f'<rect width="{w}" height="{h}" rx="28" fill="{background}" />',
        f'<rect x="0" y="0" width="{w}" height="8" rx="8" fill="{accent}" />',
    ]
    cursor_y = 50
    if eyebrow:
        fragments.append(
            text_block(
                34,
                cursor_y,
                [eyebrow],
                size=14,
                line_height=16,
                fill=eyebrow_fill,
                weight=700,
                letter_spacing=1.5,
                opacity=0.95,
            )
        )
        cursor_y += 28

    fragments.append(text_block(34, cursor_y, [title], size=28, line_height=34, fill=title_fill, weight=700))
    cursor_y += 22
    fragments.append(f'<line x1="34" y1="{cursor_y}" x2="{w - 34}" y2="{cursor_y}" stroke="{divider}" stroke-width="1.5" />')
    cursor_y += 40

    for item in lines:
        bullet = (
            f'<circle cx="42" cy="{cursor_y - 8}" r="5" fill="{accent}" />'
            if item.startswith("• ")
            else ""
        )
        body_lines = [item[2:]] if item.startswith("• ") else [item]
        text_x = 58 if bullet else 34
        fragments.append(bullet)
        fragments.append(
            text_block(
                text_x,
                cursor_y,
                body_lines,
                size=22,
                line_height=30,
                fill=body_fill,
                weight=500,
            )
        )
        cursor_y += 48

    fragments.append("</g>")
    return "".join(fragments)


def stat_panel(
    x: int,
    y: int,
    w: int,
    h: int,
    value: str,
    label: str,
    note: str,
    *,
    accent: str | None = None,
) -> str:
    accent = accent or COLORS["orange"]
    return (
        f'<g transform="translate({x} {y})" filter="url(#card-shadow)">'
        f'<rect width="{w}" height="{h}" rx="30" fill="{COLORS["dark"]}" />'
        f'<circle cx="{w / 2}" cy="90" r="52" fill="{accent}" opacity="0.16" />'
        f'{text_block(w // 2, 102, [value], size=46, line_height=52, fill=COLORS["white"], weight=800, anchor="middle")}'
        f'{text_block(w // 2, 156, [label], size=24, line_height=30, fill=COLORS["orange"], weight=700, anchor="middle")}'
        f'{text_block(w // 2, 214, [note], size=18, line_height=24, fill="#F5EEE6", weight=500, anchor="middle")}'
        "</g>"
    )


def logo_group(x: int, y: int, *, scale: float = 1.0) -> str:
    return f"""
    <g transform="translate({x} {y}) scale({scale})">
      <circle cx="28" cy="28" r="28" fill="{COLORS["dark"]}" />
      <circle cx="28" cy="28" r="18" fill="{COLORS["orange"]}" opacity="0.18" />
      <rect x="18" y="14" width="6" height="28" rx="3" fill="{COLORS["orange"]}" />
      <rect x="32" y="14" width="6" height="28" rx="3" fill="{COLORS["orange"]}" />
      <rect x="24" y="24" width="8" height="6" rx="3" fill="{COLORS["orange"]}" />
      <text x="70" y="36" font-size="34" font-weight="800" fill="{COLORS["orange"]}" font-family="Arial, Helvetica, sans-serif">HUMBER</text>
    </g>
    """


def icon_calendar(x: int, y: int, *, scale: float = 1.0, stroke: str | None = None) -> str:
    stroke = stroke or COLORS["orange"]
    return f"""
    <g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{stroke}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
      <rect x="6" y="14" width="72" height="62" rx="12" />
      <line x1="6" y1="30" x2="78" y2="30" />
      <line x1="24" y1="4" x2="24" y2="22" />
      <line x1="60" y1="4" x2="60" y2="22" />
      <line x1="24" y1="46" x2="38" y2="46" />
      <line x1="24" y1="58" x2="38" y2="58" />
      <path d="M52 55l7 7 14-18" />
    </g>
    """


def icon_chat(x: int, y: int, *, scale: float = 1.0, stroke: str | None = None) -> str:
    stroke = stroke or COLORS["orange"]
    return f"""
    <g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{stroke}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 18h44a10 10 0 0 1 10 10v22a10 10 0 0 1-10 10H38l-14 12v-12H12A10 10 0 0 1 2 50V28a10 10 0 0 1 10-10z" />
      <circle cx="24" cy="39" r="3.5" fill="{stroke}" />
      <circle cx="39" cy="39" r="3.5" fill="{stroke}" />
      <circle cx="54" cy="39" r="3.5" fill="{stroke}" />
    </g>
    """


def icon_review(x: int, y: int, *, scale: float = 1.0, stroke: str | None = None) -> str:
    stroke = stroke or COLORS["orange"]
    return f"""
    <g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{stroke}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
      <rect x="6" y="8" width="76" height="52" rx="10" />
      <line x1="28" y1="74" x2="60" y2="74" />
      <line x1="44" y1="60" x2="44" y2="74" />
      <path d="M22 34l12 12 28-24" />
    </g>
    """


def icon_retro(x: int, y: int, *, scale: float = 1.0, stroke: str | None = None) -> str:
    stroke = stroke or COLORS["orange"]
    return f"""
    <g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{stroke}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
      <path d="M24 14a26 26 0 0 1 35 8" />
      <path d="M59 22v14H45" />
      <path d="M56 56a26 26 0 0 1-35-8" />
      <path d="M21 48V34h14" />
      <circle cx="40" cy="35" r="12" />
      <path d="M34 35h12" />
    </g>
    """


def icon_refinement(x: int, y: int, *, scale: float = 1.0, stroke: str | None = None) -> str:
    stroke = stroke or COLORS["orange"]
    return f"""
    <g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{stroke}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
      <rect x="10" y="16" width="60" height="18" rx="6" />
      <rect x="18" y="40" width="60" height="18" rx="6" />
      <rect x="26" y="64" width="60" height="18" rx="6" />
      <path d="M78 10l14 14" />
      <path d="M88 20l-12 30 9 9 30-12" />
    </g>
    """


def icon_cycle(x: int, y: int, *, scale: float = 1.0, stroke: str | None = None) -> str:
    stroke = stroke or COLORS["orange"]
    return f"""
    <g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{stroke}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="42" cy="42" r="28" />
      <path d="M42 4v14" />
      <path d="M42 66v14" />
      <path d="M4 42h14" />
      <path d="M66 42h14" />
      <path d="M55 14l9 9-9 9" />
      <path d="M29 70l-9-9 9-9" />
    </g>
    """


def defs() -> str:
    return f"""
    <defs>
      <linearGradient id="hero-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{COLORS["orange_soft"]}" />
        <stop offset="100%" stop-color="{COLORS["white"]}" />
      </linearGradient>
      <linearGradient id="dark-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{COLORS["dark"]}" />
        <stop offset="100%" stop-color="{COLORS["graphite"]}" />
      </linearGradient>
      <filter id="card-shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#120F10" flood-opacity="0.08" />
      </filter>
    </defs>
    """


def background(page_number: int) -> str:
    return f"""
    <rect width="{WIDTH}" height="{HEIGHT}" fill="{COLORS["cream"]}" />
    <circle cx="1380" cy="110" r="190" fill="{COLORS["orange"]}" opacity="0.10" />
    <circle cx="1420" cy="760" r="250" fill="{COLORS["dark"]}" opacity="0.06" />
    <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="url(#hero-gradient)" opacity="0.35" />
    <path d="M1050 0h550v180c-120 35-238 27-352-26-95-43-161-87-198-154z" fill="{COLORS["white"]}" opacity="0.50" />
    <path d="M0 755c131 38 252 53 365 42 125-11 243-52 352-121 123-78 230-112 325-104 131 12 240 81 558 328H0z" fill="{COLORS["white"]}" opacity="0.82" />
    <line x1="100" y1="146" x2="1490" y2="146" stroke="{COLORS["line"]}" stroke-width="2" />
    {text_block(1500, 92, [f"{page_number:02d}"], size=28, line_height=32, fill=COLORS["muted"], weight=700, anchor="end")}
    {text_block(1500, 124, ["Humber x Scrum"], size=14, line_height=18, fill=COLORS["orange_dark"], weight=700, anchor="end", letter_spacing=1.4)}
    {logo_group(88, 54, scale=0.9)}
    """


def slide_shell(
    page_number: int,
    title_lines: list[str],
    subtitle_lines: list[str],
    body: str,
    *,
    eyebrow: str = "CEREMONIAS SCRUM",
    title_size: int = 58,
    title_y: int = 230,
    subtitle_y: int = 330,
) -> str:
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
      {defs()}
      {background(page_number)}
      {text_block(92, 182, [eyebrow], size=15, line_height=18, fill=COLORS["orange_dark"], weight=800, letter_spacing=2.0)}
      {text_block(92, title_y, title_lines, size=title_size, line_height=70, fill=COLORS["dark"], weight=800)}
      {text_block(92, subtitle_y, subtitle_lines, size=28, line_height=36, fill=COLORS["muted"], weight=500)}
      {body}
    </svg>
    """


def cover_slide() -> str:
    nodes = [
        (1070, 308, "Sprint", "Planning", COLORS["orange_soft"], COLORS["dark"]),
        (1320, 408, "Daily", "Scrum", COLORS["dark"], COLORS["white"]),
        (1225, 650, "Sprint", "Review", COLORS["white"], COLORS["dark"]),
        (965, 566, "Retro", "spective", COLORS["white"], COLORS["dark"]),
    ]
    node_markup = []
    for x, y, line_a, line_b, fill, text_fill in nodes:
        node_markup.append(
            f'<g transform="translate({x} {y})" filter="url(#card-shadow)">'
            f'<circle cx="0" cy="0" r="82" fill="{fill}" stroke="{COLORS["orange"]}" stroke-width="2.5" />'
            f'{text_block(0, -6, [line_a, line_b], size=24, line_height=28, fill=text_fill, weight=700, anchor="middle")}'
            "</g>"
        )

    body = f"""
      {text_block(92, 252, ["Guía visual para explicar el marco de trabajo, sus eventos y el valor", "que aporta cada ceremonia dentro del ciclo ágil de Humber."], size=29, line_height=40, fill=COLORS["ink"], weight=500)}
      {chip(92, 428, "Sprint como contenedor", fill=COLORS["orange_soft"], text_fill=COLORS["dark"], stroke=COLORS["orange"])}
      {chip(340, 428, "Iteración + aprendizaje", fill=COLORS["white"], text_fill=COLORS["dark"], stroke=COLORS["line"])}
      {chip(598, 428, "Foco en valor de negocio", fill=COLORS["white"], text_fill=COLORS["dark"], stroke=COLORS["line"])}

      <g filter="url(#card-shadow)">
        <rect x="900" y="220" width="560" height="500" rx="42" fill="url(#dark-gradient)" />
        <circle cx="1180" cy="470" r="116" fill="{COLORS["orange"]}" opacity="0.18" />
        <circle cx="1180" cy="470" r="88" fill="{COLORS["orange"]}" opacity="0.16" stroke="{COLORS["orange"]}" stroke-width="2" />
        {icon_cycle(1138, 428, scale=1.0, stroke=COLORS["orange"])}
        {text_block(1180, 492, ["SPRINT"], size=30, line_height=36, fill=COLORS["white"], weight=800, anchor="middle", letter_spacing=1.8)}
        {"".join(node_markup)}
      </g>

      <g filter="url(#card-shadow)">
        <rect x="92" y="560" width="720" height="180" rx="30" fill="{COLORS["white"]}" />
        {text_block(128, 614, ["Qué vas a encontrar"], size=28, line_height=32, fill=COLORS["dark"], weight=800)}
        {text_block(128, 664, ["• Objetivo y propósito de cada ceremonia", "• Participantes, frecuencia y duración", "• Resultados concretos para guiar tu explicación"], size=22, line_height=34, fill=COLORS["ink"], weight=500)}
      </g>
    """
    return slide_shell(
        1,
        ["Metodología Scrum", "aplicada a Humber"],
        ["Ceremonias, dinámica de trabajo y puntos clave", "para una presentación clara y visual."],
        body,
        eyebrow="PRESENTACIÓN EJECUTIVA",
        title_size=72,
        title_y=200,
        subtitle_y=352,
    )


def overview_slide() -> str:
    daily_dots = "".join(
        f'<g transform="translate({300 + index * 86} 350)">'
        f'<circle cx="0" cy="0" r="18" fill="{COLORS["white"]}" stroke="{COLORS["orange"]}" stroke-width="3" />'
        f'{text_block(0, 8, [str(index + 1)], size=16, line_height=18, fill=COLORS["dark"], weight=700, anchor="middle")}'
        "</g>"
        for index in range(8)
    )
    cards = [
        panel(92, 460, 270, 250, "Sprint Planning", ["• Define meta, alcance y plan inicial.", "• Ordena prioridades y capacidad real.", "• Resultado: Sprint Goal + backlog."], accent=COLORS["orange"]),
        panel(384, 460, 270, 250, "Daily Scrum", ["• Sincroniza al equipo en 15 minutos.", "• Inspecciona avances e impedimentos.", "• Ajusta el plan diario."], accent=COLORS["orange"]),
        panel(676, 460, 270, 250, "Sprint Review", ["• Se demuestra el incremento logrado.", "• Se recoge feedback del negocio.", "• Se adapta el Product Backlog."], accent=COLORS["orange"]),
        panel(968, 460, 270, 250, "Retrospective", ["• Revisa cómo trabajó el equipo.", "• Detecta causas y aprendizajes.", "• Define mejoras accionables."], accent=COLORS["orange"]),
        panel(1260, 460, 248, 250, "Refinement", ["• Acompaña todo el sprint.", "• Aclara historias, riesgos y criterios.", "• Llega mejor preparado a planning."], accent=COLORS["orange"]),
    ]
    body = f"""
      <g filter="url(#card-shadow)">
        <rect x="92" y="250" width="1416" height="150" rx="34" fill="{COLORS["white"]}" />
        <rect x="140" y="312" width="1240" height="14" rx="7" fill="{COLORS["orange_soft"]}" />
        <rect x="140" y="312" width="1240" height="14" rx="7" fill="{COLORS["orange"]}" opacity="0.28" />
        <g transform="translate(152 282)">
          <rect width="126" height="72" rx="24" fill="{COLORS["dark"]}" />
          {text_block(63, 28, ["Inicio"], size=18, line_height=20, fill=COLORS["orange"], weight=700, anchor="middle")}
          {text_block(63, 52, ["Planning"], size=22, line_height=24, fill=COLORS["white"], weight=700, anchor="middle")}
        </g>
        {daily_dots}
        <g transform="translate(1078 282)">
          <rect width="126" height="72" rx="24" fill="{COLORS["dark"]}" />
          {text_block(63, 28, ["Cierre"], size=18, line_height=20, fill=COLORS["orange"], weight=700, anchor="middle")}
          {text_block(63, 52, ["Review"], size=22, line_height=24, fill=COLORS["white"], weight=700, anchor="middle")}
        </g>
        <g transform="translate(1230 282)">
          <rect width="126" height="72" rx="24" fill="{COLORS["orange"]}" />
          {text_block(63, 28, ["Mejora"], size=18, line_height=20, fill=COLORS["dark"], weight=700, anchor="middle")}
          {text_block(63, 52, ["Retro"], size=22, line_height=24, fill=COLORS["dark"], weight=800, anchor="middle")}
        </g>
        {text_block(145, 382, ["Refinement continuo durante todo el sprint"], size=20, line_height=24, fill=COLORS["orange_dark"], weight=700)}
      </g>
      {"".join(cards)}
    """
    return slide_shell(
        2,
        ["Mapa de ceremonias Scrum"],
        ["Vista general del flujo para explicar cuándo ocurre cada evento", "y qué aporta dentro del sprint."],
        body,
        eyebrow="VISIÓN DE CONJUNTO",
    )


def sprint_slide() -> str:
    radar = """
      <g filter="url(#card-shadow)">
        <rect x="92" y="286" width="610" height="452" rx="38" fill="url(#dark-gradient)" />
        <circle cx="398" cy="512" r="148" fill="#FFFFFF" opacity="0.06" />
        <circle cx="398" cy="512" r="104" fill="none" stroke="#F5A623" stroke-width="2.5" opacity="0.5" />
        <circle cx="398" cy="512" r="168" fill="none" stroke="#F5A623" stroke-width="1.5" opacity="0.16" />
        <circle cx="398" cy="512" r="62" fill="#F5A623" opacity="0.18" />
        <text x="398" y="492" font-size="30" font-weight="800" fill="#FFFFFF" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"><tspan x="398" dy="0">SPRINT</tspan></text>
        <text x="398" y="528" font-size="20" font-weight="600" fill="#F5A623" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"><tspan x="398" dy="0">1 a 4 semanas</tspan></text>
        <text x="398" y="558" font-size="18" font-weight="500" fill="#F5EEE6" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"><tspan x="398" dy="0">contenedor de todos</tspan><tspan x="398" dy="24">los eventos Scrum</tspan></text>
        <g transform="translate(398 336)" filter="url(#card-shadow)">
          <circle cx="0" cy="0" r="56" fill="#FFF2D8" stroke="#F5A623" stroke-width="2.5" />
          <text x="0" y="-6" font-size="18" font-weight="800" fill="#231F20" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"><tspan x="0" dy="0">Sprint</tspan><tspan x="0" dy="22">Planning</tspan></text>
        </g>
        <g transform="translate(560 476)" filter="url(#card-shadow)">
          <circle cx="0" cy="0" r="54" fill="#FFFFFF" stroke="#F5A623" stroke-width="2.5" />
          <text x="0" y="-6" font-size="18" font-weight="800" fill="#231F20" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"><tspan x="0" dy="0">Daily</tspan><tspan x="0" dy="22">Scrum</tspan></text>
        </g>
        <g transform="translate(484 660)" filter="url(#card-shadow)">
          <circle cx="0" cy="0" r="56" fill="#FFFFFF" stroke="#F5A623" stroke-width="2.5" />
          <text x="0" y="-6" font-size="18" font-weight="800" fill="#231F20" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"><tspan x="0" dy="0">Sprint</tspan><tspan x="0" dy="22">Review</tspan></text>
        </g>
        <g transform="translate(284 664)" filter="url(#card-shadow)">
          <circle cx="0" cy="0" r="56" fill="#FFF2D8" stroke="#F5A623" stroke-width="2.5" />
          <text x="0" y="-6" font-size="18" font-weight="800" fill="#231F20" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"><tspan x="0" dy="0">Retro</tspan><tspan x="0" dy="22">spective</tspan></text>
        </g>
        <g transform="translate(228 470)" filter="url(#card-shadow)">
          <circle cx="0" cy="0" r="54" fill="#231F20" stroke="#F5A623" stroke-width="2.5" />
          <text x="0" y="-6" font-size="18" font-weight="800" fill="#FFFFFF" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"><tspan x="0" dy="0">Refine</tspan><tspan x="0" dy="22">ment</tspan></text>
        </g>
      </g>
    """
    body = f"""
      {radar}
      {panel(736, 286, 356, 206, "Qué es", ["• Marco temporal fijo.", "• Busca crear un incremento usable.", "• Hace visible el progreso."], accent=COLORS["orange"])}
      {panel(1118, 286, 390, 206, "Propósito", ["• Entregar valor con frecuencia.", "• Reducir riesgo mediante inspección.", "• Aprender rápido con feedback."], accent=COLORS["orange"])}
      {panel(736, 518, 460, 220, "Reglas clave para contarlo", ["• No se extiende: si falta, se replanifica.", "• Tiene una meta clara: Sprint Goal.", "• Cada evento existe para inspeccionar y adaptar."], accent=COLORS["orange"], dark=True, eyebrow="MARCO DEL CICLO")}
      {stat_panel(1222, 518, 286, 220, "1-4", "semanas", "duración recomendada para mantener foco y previsibilidad.", accent=COLORS["orange"])}
    """
    return slide_shell(
        3,
        ["El Sprint como contenedor"],
        ["Todas las ceremonias ocurren dentro del sprint y apuntan a entregar un incremento con valor."],
        body,
        eyebrow="CEREMONIA 00",
    )


def planning_slide() -> str:
    body = f"""
      <g filter="url(#card-shadow)">
        <rect x="92" y="286" width="500" height="470" rx="36" fill="url(#dark-gradient)" />
        <circle cx="342" cy="420" r="114" fill="{COLORS["orange"]}" opacity="0.15" />
        {icon_calendar(264, 334, scale=1.35, stroke=COLORS["orange"])}
        {text_block(140, 490, ["Objetivo principal"], size=26, line_height=30, fill=COLORS["orange"], weight=800)}
        {text_block(140, 540, ["Alinear al equipo sobre el valor", "del sprint y convertir prioridades", "del backlog en un plan realista."], size=30, line_height=38, fill=COLORS["white"], weight=700)}
        {chip(140, 676, "Participan: PO + SM + Dev Team", fill=COLORS["orange_soft"], text_fill=COLORS["dark"], stroke=COLORS["orange"])}
      </g>

      {panel(626, 286, 278, 224, "Qué se define", ["• Sprint Goal.", "• Historias a tomar.", "• Criterios de terminado."], accent=COLORS["orange"])}
      {panel(930, 286, 278, 224, "Qué se revisa", ["• Prioridades de negocio.", "• Capacidad del equipo.", "• Riesgos y dependencias."], accent=COLORS["orange"])}
      {panel(1234, 286, 274, 224, "Resultado", ["• Sprint Backlog visible.", "• Plan inicial compartido.", "• Compromiso entendible."], accent=COLORS["orange"])}

      {panel(626, 536, 550, 220, "Preguntas guía", ["• ¿Por qué este sprint es valioso ahora?", "• ¿Qué ítems generan mayor impacto?", "• ¿Cómo vamos a abordar el trabajo?"], accent=COLORS["orange"], dark=False)}
      {stat_panel(1202, 536, 306, 220, "TIMEBOX", "Hasta 8 h", "en un sprint de 1 mes; menos en sprints cortos.", accent=COLORS["orange"])}
    """
    return slide_shell(
        4,
        ["Sprint Planning"],
        ["Define por qué, qué y cómo se trabajará durante el sprint."],
        body,
        eyebrow="CEREMONIA 01",
    )


def daily_slide() -> str:
    question_card_width = 408
    questions = [
        ("¿Qué hice desde la última daily?", 92),
        ("¿Qué voy a hacer hoy?", 500),
        ("¿Hay impedimentos o riesgos?", 908),
    ]
    question_cards = []
    for text, x in questions:
        question_cards.append(
            f'<g transform="translate({x} 330)" filter="url(#card-shadow)">'
            f'<rect width="{question_card_width}" height="160" rx="30" fill="{COLORS["white"]}" />'
            f'{icon_chat(28, 28, scale=0.72, stroke=COLORS["orange"])}'
            f'{text_block(112, 70, [text], size=30, line_height=36, fill=COLORS["dark"], weight=700)}'
            "</g>"
        )
    body = f"""
      {"".join(question_cards)}
      {stat_panel(92, 542, 320, 216, "15 min", "máximo", "ritmo breve, concreto y diario", accent=COLORS["orange"])}
      {panel(438, 542, 454, 216, "Buenas prácticas", ["• Hablar del plan, no del estado personal.", "• Detectar bloqueos temprano.", "• Mantener foco en el Sprint Goal."], accent=COLORS["orange"])}
      {panel(918, 542, 590, 216, "Claves para explicarla", ["• La daily es del equipo, no un reporte al jefe.", "• Si aparece un tema profundo, se trata aparte.", "• Su valor está en inspeccionar y adaptar cada día."], accent=COLORS["orange"], dark=True, eyebrow="MENSAJE CLAVE")}
    """
    return slide_shell(
        5,
        ["Daily Scrum"],
        ["Sincronización diaria para inspeccionar el avance y ajustar el plan."],
        body,
        eyebrow="CEREMONIA 02",
    )


def refinement_slide() -> str:
    backlog_cards = "".join(
        f'<g transform="translate({940 + idx * 36} {332 + idx * 60})" filter="url(#card-shadow)">'
        f'<rect width="410" height="92" rx="24" fill="{COLORS["white"]}" />'
        f'<rect x="24" y="28" width="84" height="34" rx="17" fill="{COLORS["orange_soft"]}" stroke="{COLORS["orange"]}" stroke-width="1.5" />'
        f'{text_block(66, 50, [label], size=16, line_height=18, fill=COLORS["dark"], weight=700, anchor="middle")}'
        f'{text_block(132, 44, [title], size=24, line_height=28, fill=COLORS["dark"], weight=700)}'
        f'{text_block(132, 72, [subtitle], size=18, line_height=22, fill=COLORS["muted"], weight=500)}'
        "</g>"
        for idx, (label, title, subtitle) in enumerate(
            [
                ("US-14", "Cotización multiorigen", "valor, dependencias y aceptación"),
                ("US-18", "Alertas por demora", "riesgos, prioridad y métricas"),
                ("US-21", "Dashboard operativo", "estimación y definición de listo"),
            ]
        )
    )
    body = f"""
      <g filter="url(#card-shadow)">
        <rect x="92" y="300" width="522" height="430" rx="38" fill="url(#dark-gradient)" />
        {icon_refinement(128, 338, scale=1.3, stroke=COLORS["orange"])}
        {text_block(128, 474, ["Práctica continua"], size=26, line_height=30, fill=COLORS["orange"], weight=800)}
        {text_block(128, 530, ["No es un evento formal del", "Scrum Guide, pero suele ser", "clave para llegar listos a planning."], size=32, line_height=40, fill=COLORS["white"], weight=700)}
        {text_block(128, 674, ["Se usa para aclarar historias, criterios, riesgos,", "dependencias y tamaño antes de comprometerlas."], size=22, line_height=32, fill="#F5EEE6", weight=500)}
      </g>

      {panel(646, 300, 258, 206, "Objetivo", ["• Mantener el backlog entendible.", "• Reducir incertidumbre.", "• Anticipar bloqueos."], accent=COLORS["orange"])}
      {panel(646, 524, 258, 206, "Actividades", ["• Partir historias grandes.", "• Afinar criterios.", "• Estimar y ordenar."], accent=COLORS["orange"])}
      {backlog_cards}
      {chip(932, 702, "Tip: dedicar 5% a 10% de la capacidad", fill=COLORS["orange_soft"], text_fill=COLORS["dark"], stroke=COLORS["orange"])}
    """
    return slide_shell(
        6,
        ["Backlog Refinement"],
        ["Espacio de preparación que mejora la calidad de las siguientes conversaciones."],
        body,
        eyebrow="PRÁCTICA RECOMENDADA",
    )


def review_slide() -> str:
    body = f"""
      <g filter="url(#card-shadow)">
        <rect x="92" y="294" width="610" height="442" rx="36" fill="{COLORS["white"]}" />
        <rect x="150" y="356" width="494" height="240" rx="24" fill="{COLORS["dark"]}" />
        <rect x="186" y="392" width="422" height="168" rx="18" fill="{COLORS["graphite"]}" />
        {icon_review(360, 426, scale=1.5, stroke=COLORS["orange"])}
        {text_block(396, 644, ["Demo del incremento"], size=32, line_height=38, fill=COLORS["dark"], weight=800, anchor="middle")}
        {text_block(396, 688, ["Se muestra trabajo terminado y usable.", "La conversación gira en torno al producto."], size=22, line_height=30, fill=COLORS["ink"], weight=500, anchor="middle")}
      </g>

      {panel(736, 294, 360, 194, "Participan", ["• Scrum Team completo.", "• Stakeholders relevantes.", "• Product Owner facilita visión."], accent=COLORS["orange"])}
      {panel(1122, 294, 386, 194, "Agenda sugerida", ["• Recordar Sprint Goal.", "• Demostrar el incremento.", "• Recoger feedback y próximos pasos."], accent=COLORS["orange"])}
      {panel(736, 514, 772, 222, "Resultado esperado", ["• Feedback concreto del negocio.", "• Oportunidades nuevas o cambios de prioridad.", "• Product Backlog actualizado con lo aprendido."], accent=COLORS["orange"], dark=True, eyebrow="SALIDA")}
    """
    return slide_shell(
        7,
        ["Sprint Review"],
        ["Inspección del incremento con foco en feedback real y próximos pasos de producto."],
        body,
        eyebrow="CEREMONIA 03",
    )


def retrospective_slide() -> str:
    columns = [
        ("Seguir", "Lo que funcionó y conviene preservar", 92),
        ("Dejar", "Prácticas que generan fricción o desperdicio", 382),
        ("Probar", "Experimentos concretos para mejorar", 672),
    ]
    column_markup = []
    for title, subtitle, x in columns:
        column_markup.append(
            f'<g transform="translate({x} 326)" filter="url(#card-shadow)">'
            f'<rect width="250" height="334" rx="30" fill="{COLORS["white"]}" />'
            f'<rect x="24" y="24" width="202" height="52" rx="18" fill="{COLORS["orange_soft"]}" stroke="{COLORS["orange"]}" stroke-width="1.5" />'
            f'{text_block(125, 57, [title], size=26, line_height=28, fill=COLORS["dark"], weight=800, anchor="middle")}'
            f'{text_block(32, 122, [subtitle], size=20, line_height=28, fill=COLORS["muted"], weight=500)}'
            f'{text_block(32, 208, ["• Datos y hechos", "• Causas raíz", "• Acciones viables"], size=22, line_height=38, fill=COLORS["ink"], weight=500)}'
            "</g>"
        )

    body = f"""
      {"".join(column_markup)}
      {panel(980, 326, 528, 198, "Resultado ideal", ["• 1 a 3 mejoras concretas para el próximo sprint.", "• Dueño claro por acción.", "• Fecha visible para revisar impacto."], accent=COLORS["orange"], dark=True, eyebrow="MEJORA CONTINUA")}
      {panel(980, 548, 528, 186, "Tip para presentarla", ["• No busca culpables; busca aprendizaje.", "• Cuanto más específica sea la acción, más útil será.", "• Cierra el ciclo y conecta con la próxima planning."], accent=COLORS["orange"])}
    """
    return slide_shell(
        8,
        ["Sprint Retrospective"],
        ["Espacio de reflexión del equipo para mejorar su forma de trabajar sprint a sprint."],
        body,
        eyebrow="CEREMONIA 04",
    )


def preview_logo() -> str:
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="240" height="64" viewBox="0 0 240 64">
      <rect width="240" height="64" fill="none" />
      {logo_group(0, 4, scale=1.0)}
    </svg>
    """


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    slides = {
        "01-portada.svg": cover_slide(),
        "02-mapa-scrum.svg": overview_slide(),
        "03-el-sprint.svg": sprint_slide(),
        "04-sprint-planning.svg": planning_slide(),
        "05-daily-scrum.svg": daily_slide(),
        "06-backlog-refinement.svg": refinement_slide(),
        "07-sprint-review.svg": review_slide(),
        "08-sprint-retrospective.svg": retrospective_slide(),
    }

    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    for existing_svg in SLIDES_DIR.glob("*.svg"):
        existing_svg.unlink()

    for name, svg in slides.items():
        write_file(SLIDES_DIR / name, svg)

    write_file(ASSETS_DIR / "logo-humber.svg", preview_logo())

    print(f"Generadas {len(slides)} slides en {SLIDES_DIR}")


if __name__ == "__main__":
    main()
