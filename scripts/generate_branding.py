#!/usr/bin/env python3
"""
TACE-X Falcon Emblem & Branding Asset Generator
================================================
Generates:
  1. assets/branding/tace-x-emblem.svg       (Definitive vector master)
  2. assets/branding/tace-x-emblem-white.png (Pure white silhouette on transparent background)
  3. assets/branding/tace-x-emblem.png       (Electric cyan/blue accented emblem on transparent background)
"""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BRANDING_DIR = REPO_ROOT / "assets" / "branding"
BRANDING_DIR.mkdir(parents=True, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Master Vector Falcon Insignia
# Sharp, abstract aerospace falcon:
# - Dramatic sweeping upper wing with supersonic tiered blade feathers
# - Razor-sharp tapered central stroke & predatory head silhouette
# - Sleek stabilizing lower winglet / tail blade
EMBLEM_PATHS = {
    # 1. Primary Sweeping Upper Wing Blade (The dominant sweeping arc)
    "wing_primary": (
        "M 232 142 "
        "C 285 110 355 88 442 78 "
        "C 438 112 418 152 388 184 "
        "C 346 228 296 250 252 260 "
        "C 264 228 268 190 232 142 Z"
    ),
    # 2. Secondary Sweeping Wing Blade (Aerodynamic secondary feather)
    "wing_secondary": (
        "M 258 274 "
        "C 300 262 350 240 402 198 "
        "C 388 230 364 265 330 294 "
        "C 292 326 254 338 236 342 "
        "C 246 320 252 296 258 274 Z"
    ),
    # 3. Tertiary Sweeping Wing Blade (Lower feather tier)
    "wing_tertiary": (
        "M 240 354 "
        "C 276 344 316 326 352 298 "
        "C 336 328 310 356 276 376 "
        "C 248 392 226 398 216 400 "
        "C 224 384 232 368 240 354 Z"
    ),
    # 4. Falcon Head & Tapered Central Stroke (Predatory beak, crown, spine tapering to a needle tip)
    "central_stroke_and_head": (
        "M 194 92 "
        "C 214 90 234 98 250 114 "
        "L 272 136 "
        "L 236 148 "
        "C 224 162 216 182 212 210 "
        "C 202 278 184 350 148 424 "
        "C 142 436 134 448 128 452 "
        "C 126 450 128 438 132 422 "
        "C 144 368 156 304 160 244 "
        "C 162 212 160 186 150 166 "
        "C 142 150 134 140 126 134 "
        "C 144 116 168 96 194 92 Z"
    ),
    # 5. Lower Swept Winglet / Tail Fin (Sharp aerodynamic thrust stabilizer)
    "tail_fin": (
        "M 148 278 "
        "C 158 296 162 320 158 350 "
        "C 152 384 136 422 110 460 "
        "C 102 470 94 480 88 484 "
        "C 88 478 92 464 98 448 "
        "C 112 410 126 366 130 326 "
        "C 132 302 134 286 148 278 Z"
    )
}

def create_emblem_svg(mode="accent"):
    """
    Generate master SVG for the emblem.
    mode='accent': Electric cyan / deep blue / violet gradient with glowing edges
    mode='white': Pure clean white silhouette
    """
    if mode == "white":
        fill = "#FFFFFF"
        defs = ""
    else:
        defs = """
    <defs>
      <linearGradient id="falconGradient" x1="100" y1="80" x2="440" y2="460" gradientUnits="userSpaceOnUse">
        <stop offset="0%" stop-color="#00F0FF" />
        <stop offset="25%" stop-color="#38BDF8" />
        <stop offset="65%" stop-color="#2563EB" />
        <stop offset="100%" stop-color="#8B5CF6" />
      </linearGradient>
      <filter id="emblemGlow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="8" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>
"""
        fill = "url(#falconGradient)"

    paths_markup = "\n".join([f'    <path d="{d}" fill="{fill}" />' for d in EMBLEM_PATHS.values()])

    svg = f"""<svg width="512" height="512" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>TACE-X Falcon Emblem</title>
  <desc>Sharp abstract falcon emblem with sweeping upper wing and tapered central stroke.</desc>
{defs}
  <g>
{paths_markup}
  </g>
</svg>
"""
    return svg


def render_svg_to_png(svg_string, png_path, size=1024):
    """Render SVG to transparent PNG using headless Chrome."""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {{
    margin: 0;
    padding: 0;
    width: {size}px;
    height: {size}px;
    background: transparent;
    overflow: hidden;
  }}
  svg {{
    width: {size}px;
    height: {size}px;
    display: block;
  }}
</style>
</head>
<body>
{svg_string}
</body>
</html>
"""
    tmp_html = BRANDING_DIR / "_tmp_render.html"
    tmp_html.write_text(html_content, encoding="utf-8")

    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        f"--window-size={size},{size}",
        "--default-background-color=00000000",
        f"--screenshot={str(png_path)}",
        str(tmp_html)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if tmp_html.exists():
        tmp_html.unlink()


def main():
    print("[*] Generating master vector branding assets...")

    accent_svg = create_emblem_svg(mode="accent")
    svg_path = BRANDING_DIR / "tace-x-emblem.svg"
    svg_path.write_text(accent_svg, encoding="utf-8")
    print(f"  ✓ {svg_path.relative_to(REPO_ROOT)} ({svg_path.stat().st_size} bytes)")

    accent_png = BRANDING_DIR / "tace-x-emblem.png"
    render_svg_to_png(accent_svg, accent_png, size=1024)
    print(f"  ✓ {accent_png.relative_to(REPO_ROOT)} ({accent_png.stat().st_size / 1024:.1f} KB, 1024x1024 transparent)")

    white_svg = create_emblem_svg(mode="white")
    white_png = BRANDING_DIR / "tace-x-emblem-white.png"
    render_svg_to_png(white_svg, white_png, size=1024)
    print(f"  ✓ {white_png.relative_to(REPO_ROOT)} ({white_png.stat().st_size / 1024:.1f} KB, 1024x1024 transparent)")

    print("[+] All branding emblem assets generated successfully.")


if __name__ == "__main__":
    main()
