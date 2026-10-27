#!/usr/bin/env python3
"""
TACE-X Hero Card Generator
===========================
Produces a single polished hero card SVG:
  - Near-black background with subtle grid texture
  - Recognizable, coherent pixel-art portrait of Immanuel Melbin (left side)
  - Typography identity block (right side)
  - Compact verified tech strip
  - Strong arcade-inspired aesthetic

Usage:
    python3 scripts/generate_hero.py [--portrait assets/portrait/portrait_raw.png]
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageEnhance
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# ─── COLOR PALETTE ──────────────────────────────────────────────────────────
PALETTE = {
    "VOID":       (11,  15,  23),   # #0B0F17
    "DARK":       (7,   10,  15),   # #070A0F
    "SHADOW":     (17,  28,  45),   # #111C2D
    "MID":        (30,  41,  59),   # #1E293B
    "CYAN":       (0,   240, 255),  # #00F0FF
    "CYAN_DIM":   (56,  189, 248),  # #38BDF8
    "MINT":       (16,  185, 129),  # #10B981
    "MINT_DIM":   (110, 231, 183),  # #6EE7B7
    "VIOLET":     (139, 92,  246),  # #8B5CF6
    "WHITE":      (248, 250, 252),  # #F8FAFC
    "MUTED":      (148, 163, 184),  # #94A3B8
    "SLATE":      (100, 116, 139),  # #64748B
    "AMBER":      (245, 158, 11),   # #F59E0B
}

# Coherent Likeness Palette (Preserves true skin, hair, and clothing tones)
PORTRAIT_PALETTE = [
    (11,  15,  23),   # 0: VOID background
    (22,  20,  24),   # 1: HAIR_DARK (near-black wavy hair)
    (38,  32,  36),   # 2: HAIR_MID
    (55,  46,  50),   # 3: HAIR_LIGHT
    (75,  42,  25),   # 4: SKIN_DEEP (jawline & neck shadows)
    (105, 62,  40),   # 5: SKIN_SHADOW
    (138, 86,  58),   # 6: SKIN_LOW_MID
    (168, 108, 76),   # 7: SKIN_MID (natural warm South Asian complexion)
    (195, 134, 98),   # 8: SKIN_LIGHT
    (218, 162, 128),  # 9: SKIN_HIGHLIGHT
    (235, 188, 158),  # 10: SKIN_SPECULAR
    (130, 145, 165),  # 11: SHIRT_SHADOW
    (190, 202, 218),  # 12: SHIRT_MID
    (248, 250, 252),  # 13: SHIRT_WHITE (crisp white collar)
    (13,  17,  23),   # 14: SUIT_BLACK (sharp black blazer)
    (25,  33,  44),   # 15: SUIT_MID
    (42,  54,  72),   # 16: SUIT_EDGE
]


def hex_of(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def isolate_subject(img):
    """
    Isolate the portrait subject from a studio grey gradient background
    by flood-filling the outer neutral background area.
    """
    w, h = img.size
    visited = set()
    queue = [(0, 0), (w - 1, 0), (0, 10), (w - 1, 10), (1, 1), (w - 2, 1), (0, 5), (w - 1, 5)]

    def is_bg(x, y):
        if not (0 <= x < w and 0 <= y < h):
            return False
        r, g, b = img.getpixel((x, y))[:3]
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        is_neutral = max(abs(r - g), abs(g - b), abs(r - b)) < 25
        if lum < 45:
            return False  # hair or suit
        if r > g + 28:
            return False  # warm skin tone
        return is_neutral and 50 <= lum <= 145

    for qx, qy in queue:
        if is_bg(qx, qy):
            visited.add((qx, qy))

    frontier = list(visited)
    while frontier:
        cx, cy = frontier.pop()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
            nx, ny = cx + dx, cy + dy
            if (nx, ny) not in visited and is_bg(nx, ny):
                visited.add((nx, ny))
                frontier.append((nx, ny))

    out_img = Image.new("RGB", (w, h), PALETTE["VOID"])
    for y in range(h):
        for x in range(w):
            if (x, y) not in visited:
                out_img.putpixel((x, y), img.getpixel((x, y))[:3])
    return out_img


def quantize_portrait_pixel(r, g, b):
    """Map an RGB pixel to the closest likeness palette token."""
    if r < 18 and g < 22 and b < 28:
        return PALETTE["VOID"]

    best_c = PORTRAIT_PALETTE[0]
    best_d = float("inf")
    for c in PORTRAIT_PALETTE:
        cr, cg, cb = c
        d = 0.3 * (r - cr) ** 2 + 0.59 * (g - cg) ** 2 + 0.11 * (b - cb) ** 2
        if d < best_d:
            best_d = d
            best_c = c
    return best_c


def process_portrait(image_path, grid_w=48, grid_h=60):
    """
    Load, isolate background, crop to 4:5 aspect ratio, and quantize into
    a pixel-art grid that preserves facial features and recognizability.
    """
    if not HAS_PIL or not os.path.exists(image_path):
        return None

    raw_img = Image.open(image_path).convert("RGB")
    isolated = isolate_subject(raw_img)

    w, h = isolated.size
    target_aspect = grid_w / grid_h  # 48 / 60 = 0.8
    crop_w = int(h * target_aspect)
    crop_h = h
    left = max(0, (w - crop_w) // 2)
    top = 0
    crop = isolated.crop((left, top, left + crop_w, top + crop_h))

    small = crop.resize((grid_w, grid_h), Image.Resampling.LANCZOS)
    small = ImageEnhance.Contrast(small).enhance(1.15)
    small = ImageEnhance.Sharpness(small).enhance(1.2)

    grid = []
    for y in range(grid_h):
        row = []
        for x in range(grid_w):
            r, g, b = small.getpixel((x, y))
            row.append(quantize_portrait_pixel(r, g, b))
        grid.append(row)
    return grid


def build_portrait_svg_rects(grid, ox, oy, px_size=4):
    """
    Render pixel-art grid as grouped SVG rectangles at offset (ox, oy).
    Void background pixels are omitted to let the card background show through.
    """
    lines = []
    color_cells = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == PALETTE["VOID"]:
                continue
            key = hex_of(col)
            if key not in color_cells:
                color_cells[key] = []
            color_cells[key].append((ox + x * px_size, oy + y * px_size))

    cell_w = px_size - 0.4
    cell_h = px_size - 0.4

    for hex_col, cells in color_cells.items():
        lines.append(f'  <g fill="{hex_col}">')
        for cx, cy in cells:
            lines.append(f'    <rect x="{cx:.1f}" y="{cy:.1f}" width="{cell_w:.1f}" height="{cell_h:.1f}" rx="0.5"/>')
        lines.append("  </g>")
    return lines


def generate_hero_svg(portrait_path=None, output_path="assets/hero.svg"):
    """Generate the minimal, brutal, visual-first hero card SVG."""
    W, H = 900, 320

    # Portrait grid: 48 cols × 60 rows @ 4px/cell = 192 × 240 px
    GRID_W, GRID_H = 48, 60
    PX = 4
    PORT_W = GRID_W * PX   # 192
    PORT_H = GRID_H * PX   # 240
    PORT_X = 54
    PORT_Y = (H - PORT_H) // 2  # 40

    portrait_grid = None
    has_portrait = False
    if portrait_path and os.path.exists(portrait_path):
        portrait_grid = process_portrait(portrait_path, GRID_W, GRID_H)
        has_portrait = portrait_grid is not None

    lines = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">',
        f'  <title>IMMANUEL MELBIN (@tace-x) — Software · Systems · AI</title>',
        f'  <desc>Developer identity card for Immanuel Melbin (@tace-x). Builder of native terminal systems, AI platforms, and high-performance software.</desc>',
        '',
        '  <defs>',
        '    <!-- Background gradient -->',
        '    <linearGradient id="bg" x1="0" y1="0" x2="900" y2="320" gradientUnits="userSpaceOnUse">',
        '      <stop stop-color="#0B0F17"/>',
        '      <stop offset="0.5" stop-color="#070A0F"/>',
        '      <stop offset="1" stop-color="#030508"/>',
        '    </linearGradient>',
        '    <!-- Top accent line -->',
        '    <linearGradient id="accentLine" x1="0" y1="0" x2="900" y2="0" gradientUnits="userSpaceOnUse">',
        '      <stop stop-color="#00F0FF" stop-opacity="0"/>',
        '      <stop offset="0.15" stop-color="#00F0FF"/>',
        '      <stop offset="0.5" stop-color="#10B981"/>',
        '      <stop offset="0.85" stop-color="#8B5CF6"/>',
        '      <stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/>',
        '    </linearGradient>',
        '    <!-- Glow filters -->',
        '    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">',
        '      <feGaussianBlur stdDeviation="3" result="blur"/>',
        '      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        '    </filter>',
        '    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">',
        '      <feGaussianBlur stdDeviation="12"/>',
        '    </filter>',
        '    <!-- Fine grid pattern -->',
        '    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">',
        '      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#FFFFFF" stroke-opacity="0.02" stroke-width="0.8"/>',
        '    </pattern>',
        '    <clipPath id="mainClip"><rect width="900" height="320" rx="16"/></clipPath>',
        f'    <clipPath id="portClip"><rect x="{PORT_X}" y="{PORT_Y}" width="{PORT_W}" height="{PORT_H}" rx="4"/></clipPath>',
        '  </defs>',
        '',
        '  <!-- === BASE === -->',
        '  <rect width="900" height="320" rx="16" fill="url(#bg)" stroke="#1E293B" stroke-width="1.5"/>',
        '  <g clip-path="url(#mainClip)">',
        '    <rect width="900" height="320" fill="url(#grid)"/>',
        f'    <circle cx="{PORT_X + PORT_W // 2}" cy="160" r="140" fill="#00F0FF" fill-opacity="0.035" filter="url(#softGlow)"/>',
        '    <circle cx="720" cy="160" r="120" fill="#8B5CF6" fill-opacity="0.04" filter="url(#softGlow)"/>',
        '  </g>',
        '',
        '  <!-- === TOP STATUS BAR === -->',
        '  <rect x="0" y="0" width="900" height="38" fill="#070A0F" opacity="0.8"/>',
        '  <line x1="0" y1="38" x2="900" y2="38" stroke="url(#accentLine)" stroke-width="1.2"/>',
        '  <circle cx="22" cy="19" r="4" fill="#10B981" filter="url(#glow)"/>',
        '  <text x="34" y="24" fill="#64748B" font-family="\'JetBrains Mono\', monospace" font-size="11" font-weight="700" letter-spacing="2.5">TACE-X</text>',
        '  <text x="860" y="24" text-anchor="end" fill="#475569" font-family="\'JetBrains Mono\', monospace" font-size="10" letter-spacing="1.5">GITHUB.COM/TACE-X</text>',
        '',
    ]

    # === PORTRAIT SECTION ===
    lines.append('  <!-- === PORTRAIT SECTION === -->')
    port_panel_x = PORT_X - 8
    port_panel_y = PORT_Y - 8
    port_panel_w = PORT_W + 16
    port_panel_h = PORT_H + 16
    lines.append(f'  <rect x="{port_panel_x}" y="{port_panel_y}" width="{port_panel_w}" height="{port_panel_h}" rx="6" fill="#070A0F" stroke="#1E293B" stroke-width="1"/>')

    if has_portrait:
        lines.append(f'  <!-- Pixel-art portrait: {GRID_W}×{GRID_H} grid from actual headshot -->')
        lines.append('  <g clip-path="url(#portClip)">')
        portrait_rects = build_portrait_svg_rects(portrait_grid, PORT_X, PORT_Y, PX)
        lines.extend(portrait_rects)
        lines.append('  </g>')
    else:
        lines.append(f'  <rect x="{PORT_X}" y="{PORT_Y}" width="{PORT_W}" height="{PORT_H}" rx="4" fill="#111C2D"/>')
        lines.append(f'  <text x="{PORT_X + PORT_W//2}" y="{PORT_Y + PORT_H//2 + 6}" text-anchor="middle" fill="#475569" font-family="monospace" font-size="11">PORTRAIT</text>')

    # Corner brackets
    bx, by = PORT_X, PORT_Y
    bw, bh = PORT_W, PORT_H
    bracket = 16
    lines += [
        '  <!-- Corner HUD brackets -->',
        f'  <path d="M {bx} {by + bracket} L {bx} {by} L {bx + bracket} {by}" stroke="#00F0FF" stroke-width="1.5" stroke-linecap="round"/>',
        f'  <path d="M {bx + bw - bracket} {by} L {bx + bw} {by} L {bx + bw} {by + bracket}" stroke="#00F0FF" stroke-width="1.5" stroke-linecap="round"/>',
        f'  <path d="M {bx} {by + bh - bracket} L {bx} {by + bh} L {bx + bracket} {by + bh}" stroke="#10B981" stroke-width="1.5" stroke-linecap="round"/>',
        f'  <path d="M {bx + bw - bracket} {by + bh} L {bx + bw} {by + bh} L {bx + bw} {by + bh - bracket}" stroke="#10B981" stroke-width="1.5" stroke-linecap="round"/>',
    ]

    label_y = PORT_Y + PORT_H + 20
    lines += [
        f'  <text x="{PORT_X + PORT_W // 2}" y="{label_y}" text-anchor="middle" fill="#475569" font-family="\'JetBrains Mono\', monospace" font-size="9" letter-spacing="3">TACE-X // ID</text>',
    ]

    # === IDENTITY BLOCK ===
    TX = PORT_X + PORT_W + 40

    lines += [
        '',
        '  <!-- === IDENTITY BLOCK === -->',
        f'  <text x="{TX}" y="78" fill="#10B981" font-family="\'JetBrains Mono\', monospace" font-size="11" font-weight="800" letter-spacing="4">SOFTWARE  ·  SYSTEMS  ·  AI</text>',
        f'  <text x="{TX}" y="136" fill="#F8FAFC" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="54" font-weight="900" letter-spacing="-1.5">IMMANUEL</text>',
        f'  <text x="{TX}" y="192" fill="#F8FAFC" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="54" font-weight="900" letter-spacing="-1.5">MELBIN</text>',
        f'  <line x1="{TX}" y1="202" x2="{TX + 220}" y2="202" stroke="#00F0FF" stroke-width="2" stroke-opacity="0.6"/>',
        f'  <text x="{TX}" y="228" fill="#38BDF8" font-family="\'JetBrains Mono\', monospace" font-size="14" font-weight="700" letter-spacing="1">@tace-x</text>',
        f'  <text x="{TX}" y="256" fill="#94A3B8" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="14" font-weight="400">Building native terminal systems, AI platforms,</text>',
        f'  <text x="{TX}" y="275" fill="#94A3B8" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="14" font-weight="400">and high-performance software from first principles.</text>',
    ]

    # === TECH STRIP ===
    TECH_Y = 300
    TECH_START = TX

    techs = [
        ("Rust", "#F59E0B"),
        ("TypeScript", "#38BDF8"),
        ("React", "#06B6D4"),
        ("AI / NIM", "#10B981"),
        ("Firebase", "#F59E0B"),
        ("WebRTC", "#8B5CF6"),
    ]

    lines.append('  <!-- === TECH STRIP === -->')
    cx_cur = TECH_START
    for tech_name, tech_color in techs:
        text_len = len(tech_name) * 7.5 + 20
        lines += [
            f'  <rect x="{cx_cur:.0f}" y="{TECH_Y - 14}" width="{text_len:.0f}" height="18" rx="9" fill="{tech_color}" fill-opacity="0.12" stroke="{tech_color}" stroke-opacity="0.35" stroke-width="1"/>',
            f'  <text x="{cx_cur + text_len / 2:.0f}" y="{TECH_Y - 1}" text-anchor="middle" fill="{tech_color}" font-family="\'JetBrains Mono\', monospace" font-size="9.5" font-weight="700" letter-spacing="1">{tech_name}</text>',
        ]
        cx_cur += text_len + 10

    # === BOTTOM BASELINE ===
    lines += [
        '',
        '  <!-- === BASELINE === -->',
        '  <line x1="40" y1="308" x2="860" y2="308" stroke="#1E293B" stroke-width="1"/>',
        '  <text x="40" y="317" fill="#334155" font-family="\'JetBrains Mono\', monospace" font-size="9" letter-spacing="1.5">USEFUL BEFORE IMPRESSIVE  ·  ZERO SPECULATIVE BLOAT  ·  SOVEREIGN DATA</text>',
        '',
        '</svg>',
    ]

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(lines)
    output.write_text(content, encoding="utf-8")
    size_kb = output.stat().st_size / 1024
    print(f"[✓] Hero SVG generated → {output} ({size_kb:.1f} KB)")
    return str(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate TACE-X hero card SVG")
    parser.add_argument("--portrait", "-p", type=str, default="assets/portrait/portrait_raw.png", help="Path to source portrait image")
    parser.add_argument("--output", "-o", type=str, default="assets/hero.svg")
    args = parser.parse_args()
    generate_hero_svg(portrait_path=args.portrait, output_path=args.output)
