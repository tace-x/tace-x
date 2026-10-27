#!/usr/bin/env python3
"""
TACE-X Dot-Matrix Portrait & Particle-Assembly Generator
======================================================
Reproducible pipeline that:
  1. Validates and loads a source portrait or generates a high-definition
     geometric/cybernetic developer emblem fallback when no photo is provided.
  2. Crops, resizes, and enhances contrast for dot-matrix reproduction.
  3. Quantizes colors into the verified TACE-X Cyber/Neon 8-color palette.
  4. Generates a static SVG dot-matrix portrait with cybernetic HUD frame.
  5. Generates a high-resolution static PNG preview.
  6. Generates a multi-phase animated particle-assembly GIF (dispersal -> snap -> scanline -> settled).
  7. Validates asset integrity and bounded file budgets.

Author: TACE-X Engineering
Phase: 2 (Pixel-Art Identity & Futuristic Hero)
"""

import argparse
import hashlib
import json
import math
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

# ==============================================================================
# DESIGN SYSTEM COLOR PALETTE (Obsidian / Neon Tokens)
# ==============================================================================
PALETTE = {
    "VOID": (11, 15, 23),          # #0B0F17 - Deepest Obsidian Void
    "DARK_CYANITE": (7, 10, 15),    # #070A0F - Secondary Dark
    "SHADOW": (17, 28, 45),        # #111C2D - Deep Slate Shadow
    "MID_SHADOW": (30, 41, 59),    # #1E293B - Mid Wireframe Slate
    "CYAN": (0, 240, 255),         # #00F0FF - Electric Cyan
    "MINT": (16, 185, 129),        # #10B981 - Arcade Mint
    "VIOLET": (139, 92, 246),      # #8B5CF6 - Deep Space Violet
    "RED": (244, 63, 94),          # #F43F5E - Cyber Threat Red
    "WHITE": (248, 250, 252),      # #F8FAFC - Ghost White
    "AMBER": (245, 158, 11),       # #F59E0B - Secondary Accent
}

HEX_PALETTE = {
    "VOID": "#0B0F17",
    "DARK_CYANITE": "#070A0F",
    "SHADOW": "#111C2D",
    "MID_SHADOW": "#1E293B",
    "CYAN": "#00F0FF",
    "MINT": "#10B981",
    "VIOLET": "#8B5CF6",
    "RED": "#F43F5E",
    "WHITE": "#F8FAFC",
    "AMBER": "#F59E0B",
}

# ==============================================================================
# GEOMETRIC CYBERNETIC EMBLEM GENERATOR (Fallback when no photo uploaded)
# ==============================================================================
def generate_cybernetic_architect_grid(grid_size=64):
    """
    Synthesizes a bespoke 64x64 cybernetic architect silhouette emblem.
    Used when a personal portrait photo has not yet been uploaded.
    Clearly represents the TACE-X developer persona:
    - Angular obsidian head & neck silhouette
    - Glowing electric cyan visor & HUD scanning array
    - Deep violet neural lattice and cranium data paths
    - Arcade mint telemetry bus tracing down the neck
    - Threat red comms beacon on the ear/temple
    - Matrix particles in background
    """
    grid = [[PALETTE["VOID"] for _ in range(grid_size)] for _ in range(grid_size)]

    center_x = grid_size // 2
    center_y = grid_size // 2

    # Draw cranium & head profile (facing right, angular cyber-silhouette)
    # Head boundary points
    for y in range(8, 56):
        for x in range(10, 54):
            dx = x - (center_x - 1)
            dy = y - (center_y - 2)

            # Head dome (top ellipse)
            if y < 32:
                # Elliptical cranium
                dist = (dx * dx) / (15.5 * 15.5) + (dy * dy) / (14.0 * 14.0)
                if dist <= 1.0:
                    grid[y][x] = PALETTE["SHADOW"]
                    # Inner skull volume
                    if dist <= 0.75:
                        grid[y][x] = PALETTE["MID_SHADOW"]

            # Face & jaw (angular front profile)
            elif y >= 32 and y < 46:
                # Right boundary slopes back toward jaw
                right_bound = 32 - int((y - 32) * 0.45)
                left_bound = 16 + int((y - 32) * 0.2)
                if left_bound <= x <= right_bound:
                    grid[y][x] = PALETTE["SHADOW"]
                    if left_bound + 2 <= x <= right_bound - 2:
                        grid[y][x] = PALETTE["MID_SHADOW"]

            # Neck and collar
            elif y >= 46:
                neck_left = 20 - int((y - 46) * 0.6)
                neck_right = 31 + int((y - 46) * 1.1)
                if neck_left <= x <= neck_right:
                    grid[y][x] = PALETTE["SHADOW"]
                    if neck_left + 2 <= x <= neck_right - 2:
                        grid[y][x] = PALETTE["MID_SHADOW"]

    # 1. Electric Cyan Visor Array (horizontal HUD optics across eye plane)
    visor_y = 25
    for y in range(visor_y - 1, visor_y + 3):
        for x in range(24, 46):
            if 26 <= x <= 44:
                grid[y][x] = PALETTE["CYAN"]
            elif x in (25, 45):
                grid[y][x] = PALETTE["WHITE"]
    # Visor scanning glare accent
    grid[visor_y][36] = PALETTE["WHITE"]
    grid[visor_y][37] = PALETTE["WHITE"]
    grid[visor_y + 1][35] = PALETTE["WHITE"]

    # 2. Deep Violet Neural Lattice (cranium circuitry)
    for x in range(16, 32, 3):
        for y in range(13, 23):
            if (x + y) % 4 == 0 and grid[y][x] in (PALETTE["SHADOW"], PALETTE["MID_SHADOW"]):
                grid[y][x] = PALETTE["VIOLET"]
    # Crown data node
    grid[11][26] = PALETTE["VIOLET"]
    grid[11][27] = PALETTE["VIOLET"]
    grid[12][26] = PALETTE["WHITE"]

    # 3. Arcade Mint Telemetry Bus (tracing down jaw and neck)
    for y in range(32, 54):
        x_bus = 25 - int((y - 32) * 0.25)
        if 0 <= x_bus < grid_size:
            grid[y][x_bus] = PALETTE["MINT"]
            if y % 3 == 0 and x_bus + 1 < grid_size:
                grid[y][x_bus + 1] = PALETTE["MINT"]
    # Secondary parallel mint trace
    for y in range(40, 52):
        x_bus2 = 28 - int((y - 40) * 0.2)
        if 0 <= x_bus2 < grid_size:
            grid[y][x_bus2] = PALETTE["MINT"]

    # 4. Cyber Threat Red Comms / Ear Beacon
    ear_x, ear_y = 20, 29
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if 0 <= ear_y + dy < grid_size and 0 <= ear_x + dx < grid_size:
                grid[ear_y + dy][ear_x + dx] = PALETTE["RED"]
    grid[ear_y][ear_x] = PALETTE["WHITE"]

    # 5. Angular Chin & Nose highlights
    grid[35][42] = PALETTE["CYAN"]  # Nose tip
    grid[36][41] = PALETTE["CYAN"]
    grid[43][33] = PALETTE["CYAN"]  # Jaw apex
    grid[44][32] = PALETTE["CYAN"]

    # 6. Ambient Matrix Particles in Background (subtle telemetry nodes)
    telemetry_points = [
        (8, 12, PALETTE["CYAN"]),
        (52, 10, PALETTE["MINT"]),
        (10, 48, PALETTE["VIOLET"]),
        (50, 46, PALETTE["CYAN"]),
        (54, 28, PALETTE["MINT"]),
        (7, 30, PALETTE["MID_SHADOW"]),
        (48, 18, PALETTE["MID_SHADOW"]),
        (14, 8, PALETTE["MID_SHADOW"]),
    ]
    for px, py, pcol in telemetry_points:
        if 0 <= px < grid_size and 0 <= py < grid_size:
            grid[py][px] = pcol

    return grid


# ==============================================================================
# IMAGE PROCESSING & QUANTIZATION PIPELINE
# ==============================================================================
def isolate_portrait_subject(img):
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


LIKENESS_PALETTE = [
    PALETTE["VOID"],
    (22,  20,  24),   # HAIR_DARK
    (42,  34,  38),   # HAIR_MID
    (75,  42,  25),   # SKIN_DEEP
    (105, 62,  40),   # SKIN_SHADOW
    (138, 86,  58),   # SKIN_LOW_MID
    (168, 108, 76),   # SKIN_MID
    (195, 134, 98),   # SKIN_LIGHT
    (218, 162, 128),  # SKIN_HIGHLIGHT
    (235, 188, 158),  # SKIN_SPECULAR
    (130, 145, 165),  # SHIRT_SHADOW
    (190, 202, 218),  # SHIRT_MID
    PALETTE["WHITE"],  # SHIRT_WHITE
    (13,  17,  23),   # SUIT_BLACK
    (25,  33,  44),   # SUIT_MID
    (42,  54,  72),   # SUIT_EDGE
]


def process_source_image(image_path, grid_size=64):
    """
    Loads, square-crops, enhances, and quantizes a source portrait image
    into a 64x64 grid of colors preserving recognizability and natural tones.
    """
    raw = Image.open(image_path).convert("RGB")
    isolated = isolate_portrait_subject(raw)

    w, h = isolated.size
    crop_size = min(w, h)
    left = (w - crop_size) // 2
    top = (h - crop_size) // 2
    img = isolated.crop((left, top, left + crop_size, top + crop_size))

    # Preprocessing
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(1.15)
    sharpness_enhancer = ImageEnhance.Sharpness(img)
    img = sharpness_enhancer.enhance(1.25)

    img_grid = img.resize((grid_size, grid_size), Image.Resampling.LANCZOS)

    grid = []
    for y in range(grid_size):
        row = []
        for x in range(grid_size):
            r, g, b = img_grid.getpixel((x, y))
            # Background void check
            if r < 18 and g < 22 and b < 28:
                row.append(PALETTE["VOID"])
                continue

            best_color = LIKENESS_PALETTE[0]
            min_dist = float("inf")
            for token in LIKENESS_PALETTE:
                tr, tg, tb = token
                dist = 0.3 * (r - tr) ** 2 + 0.59 * (g - tg) ** 2 + 0.11 * (b - tb) ** 2
                if dist < min_dist:
                    min_dist = dist
                    best_color = token
            row.append(best_color)
        grid.append(row)

    return grid


# ==============================================================================
# SVG GENERATOR (Static Vector Dot-Matrix with Cyber Frame)
# ==============================================================================
def generate_dotmatrix_svg(grid, output_path, is_fallback=False):
    """
    Renders the dot-matrix grid into a clean, lightweight, scalable SVG.
    Groups circles by color to optimize file size (<40 KB).
    Includes accessible metadata, cyber HUD frame, and reduced-motion fallback.
    """
    grid_size = len(grid)
    canvas_size = 512
    pitch = canvas_size / grid_size
    radius_base = pitch * 0.42

    # Group dots by color hex
    color_groups = {}
    for y in range(grid_size):
        for x in range(grid_size):
            color = grid[y][x]
            # Skip pure void background dots to save file size
            if color == PALETTE["VOID"]:
                continue

            # Determine radius based on importance/luminance
            if color in (PALETTE["SHADOW"], PALETTE["MID_SHADOW"]):
                r = pitch * 0.28
            elif color in (PALETTE["WHITE"], PALETTE["CYAN"]):
                r = pitch * 0.45
            else:
                r = radius_base

            cx = round(x * pitch + pitch / 2, 2)
            cy = round(y * pitch + pitch / 2, 2)
            r_val = round(r, 2)

            hex_col = "#{:02X}{:02X}{:02X}".format(*color)
            if hex_col not in color_groups:
                color_groups[hex_col] = []
            color_groups[hex_col].append((cx, cy, r_val))

    desc_text = (
        "TACE-X Cybernetic Identity — Dot-matrix geometric developer avatar"
        if is_fallback else
        "TACE-X Developer Identity — Custom dot-matrix pixel-art portrait"
    )

    svg_lines = [
        '<svg width="512" height="512" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg">',
        f'  <title>TACE-X // DEVELOPER IDENTITY MATRIX</title>',
        f'  <desc>{desc_text}</desc>',
        '  <defs>',
        '    <linearGradient id="bgGrad" x1="0" y1="0" x2="512" y2="512" gradientUnits="userSpaceOnUse">',
        '      <stop stop-color="#0B0F17"/>',
        '      <stop offset="0.6" stop-color="#070A0F"/>',
        '      <stop offset="1" stop-color="#030508"/>',
        '    </linearGradient>',
        '    <linearGradient id="cyanBorder" x1="0" y1="0" x2="512" y2="0" gradientUnits="userSpaceOnUse">',
        '      <stop stop-color="#00F0FF" stop-opacity="0.8"/>',
        '      <stop offset="0.5" stop-color="#10B981" stop-opacity="0.5"/>',
        '      <stop offset="1" stop-color="#8B5CF6" stop-opacity="0.8"/>',
        '    </linearGradient>',
        '    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feGaussianBlur stdDeviation="3" result="glow"/>',
        '      <feMerge>',
        '        <feMergeNode in="glow"/>',
        '        <feMergeNode in="SourceGraphic"/>',
        '      </feMerge>',
        '    </filter>',
        '  </defs>',
        '  <style>',
        '    .hud-pulse { animation: hudPulse 3s ease-in-out infinite; transform-origin: center; }',
        '    @keyframes hudPulse { 0%,100% { opacity: 0.7; } 50% { opacity: 1; } }',
        '    @media (prefers-reduced-motion: reduce) { .hud-pulse { animation: none !important; } }',
        '  </style>',
        '',
        '  <!-- Background Canvas -->',
        '  <rect width="512" height="512" rx="20" fill="url(#bgGrad)"/>',
        '  <rect x="2" y="2" width="508" height="508" rx="18" fill="none" stroke="#1E293B" stroke-width="1.5"/>',
        '',
        '  <!-- Subtle Grid Backplane -->',
        '  <g stroke="#1E293B" stroke-opacity="0.25" stroke-width="0.5">',
    ]

    # Grid guide lines every 64px
    for g_pos in range(64, 512, 64):
        svg_lines.append(f'    <line x1="{g_pos}" y1="8" x2="{g_pos}" y2="504"/>')
        svg_lines.append(f'    <line x1="8" y1="{g_pos}" x2="504" y2="{g_pos}"/>')
    svg_lines.append('  </g>')
    svg_lines.append('')

    # Draw grouped circles
    svg_lines.append('  <!-- Dot Matrix Matrix -->')
    for hex_col, circles in color_groups.items():
        filter_attr = ' filter="url(#neonGlow)"' if hex_col in ("#00F0FF", "#F8FAFC", "#F43F5E") else ''
        svg_lines.append(f'  <g fill="{hex_col}"{filter_attr}>')
        for cx, cy, r_val in circles:
            svg_lines.append(f'    <circle cx="{cx}" cy="{cy}" r="{r_val}"/>')
        svg_lines.append('  </g>')

    # HUD Cybernetic Framing Elements
    svg_lines.extend([
        '',
        '  <!-- Cybernetic HUD Overlay -->',
        '  <!-- Top-Left Bracket -->',
        '  <path d="M 16 36 L 16 16 L 36 16" stroke="#00F0FF" stroke-width="2" stroke-linecap="round"/>',
        '  <!-- Top-Right Bracket -->',
        '  <path d="M 476 16 L 496 16 L 496 36" stroke="#00F0FF" stroke-width="2" stroke-linecap="round"/>',
        '  <!-- Bottom-Left Bracket -->',
        '  <path d="M 16 476 L 16 496 L 36 496" stroke="#00F0FF" stroke-width="2" stroke-linecap="round"/>',
        '  <!-- Bottom-Right Bracket -->',
        '  <path d="M 476 496 L 496 496 L 496 476" stroke="#00F0FF" stroke-width="2" stroke-linecap="round"/>',
        '',
        '  <!-- Header Telemetry Strip -->',
        '  <circle class="hud-pulse" cx="44" cy="26" r="3.5" fill="#10B981"/>',
        '  <text x="54" y="30" fill="#94A3B8" font-family="\'JetBrains Mono\', monospace" font-size="10" font-weight="700" letter-spacing="1.5">SYS: ID_MATRIX // 64x64</text>',
        '  <text x="468" y="30" text-anchor="end" fill="#00F0FF" font-family="\'JetBrains Mono\', monospace" font-size="10" font-weight="700" letter-spacing="1.5">LIVE</text>',
        '',
        '  <!-- Footer Telemetry Strip -->',
        '  <line x1="24" y1="482" x2="488" y2="482" stroke="#1E293B" stroke-width="1"/>',
        '  <text x="24" y="498" fill="#64748B" font-family="\'JetBrains Mono\', monospace" font-size="9" font-weight="700" letter-spacing="1">TACE-X // PORTRAIT MATRIX</text>',
        '  <text x="488" y="498" text-anchor="end" fill="#10B981" font-family="\'JetBrains Mono\', monospace" font-size="9" font-weight="700" letter-spacing="1">QUANTIZED // 8-COL</text>',
        '</svg>'
    ])

    svg_content = "\n".join(svg_lines)

    # Validate XML
    ET.fromstring(svg_content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    return output_path


# ==============================================================================
# ANIMATED PARTICLE ASSEMBLY GIF GENERATOR
# ==============================================================================
def generate_assembly_gif(grid, output_path, fps=15, duration_sec=2.4):
    """
    Renders an animated particle-assembly GIF:
      - Phase 1 (Frames 0-18): Particles stream smoothly from dispersed vortex
        coordinates into target grid positions via cubic ease-out.
      - Phase 2 (Frames 19-27): Holographic cyan scanline sweeps across the
        assembled portrait with transient luminescence shimmer.
      - Phase 3 (Frames 28-35): Settled portrait hold with ambient HUD pulse.
    Optimized for GitHub README rendering (<850 KB).
    """
    grid_size = len(grid)
    canvas_size = 512
    pitch = canvas_size / grid_size

    # Collect all non-void particles
    particles = []
    for y in range(grid_size):
        for x in range(grid_size):
            col = grid[y][x]
            if col == PALETTE["VOID"]:
                continue

            target_x = x * pitch + pitch / 2
            target_y = y * pitch + pitch / 2

            # Deterministic pseudo-randomness based on coordinate hash
            h_val = int(hashlib.md5(f"{x},{y}".encode()).hexdigest()[:8], 16)
            angle = (h_val % 360) * (math.pi / 180.0)
            dist = 220.0 + (h_val % 180)

            # Dispersed starting coordinate
            start_x = 256.0 + dist * math.cos(angle)
            start_y = 256.0 + dist * math.sin(angle)

            # Base radius
            if col in (PALETTE["SHADOW"], PALETTE["MID_SHADOW"]):
                r_base = pitch * 0.28
            elif col in (PALETTE["WHITE"], PALETTE["CYAN"]):
                r_base = pitch * 0.45
            else:
                r_base = pitch * 0.40

            stagger = (h_val % 5) / 10.0  # slight arrival offset 0.0 to 0.4

            particles.append({
                "gx": x,
                "gy": y,
                "color": col,
                "tx": target_x,
                "ty": target_y,
                "sx": start_x,
                "sy": start_y,
                "r": r_base,
                "stagger": stagger
            })

    total_frames = 36
    frames = []

    # Frame timing
    # 0..18: Assembly (19 frames)
    # 19..27: Scanline sweep (9 frames)
    # 28..35: Settled state (8 frames)

    for f in range(total_frames):
        # Create base frame
        im = Image.new("RGB", (canvas_size, canvas_size), PALETTE["VOID"])
        draw = ImageDraw.Draw(im)

        # Draw outer cyber frame
        draw.rounded_rectangle([2, 2, canvas_size - 3, canvas_size - 3], radius=18, outline=PALETTE["MID_SHADOW"], width=1)

        # Subtle backplane grid lines
        for g_pos in range(64, canvas_size, 64):
            draw.line([(g_pos, 8), (g_pos, canvas_size - 8)], fill=PALETTE["DARK_CYANITE"], width=1)
            draw.line([(8, g_pos), (canvas_size - 8, g_pos)], fill=PALETTE["DARK_CYANITE"], width=1)

        # Corner HUD brackets
        draw.line([(16, 36), (16, 16), (36, 16)], fill=PALETTE["CYAN"], width=2)
        draw.line([(canvas_size - 16, 36), (canvas_size - 16, 16), (canvas_size - 36, 16)], fill=PALETTE["CYAN"], width=2)
        draw.line([(16, canvas_size - 36), (16, canvas_size - 16), (36, canvas_size - 16)], fill=PALETTE["CYAN"], width=2)
        draw.line([(canvas_size - 16, canvas_size - 36), (canvas_size - 16, canvas_size - 16), (canvas_size - 36, canvas_size - 16)], fill=PALETTE["CYAN"], width=2)

        # Top status dot
        pulse_alpha = math.sin((f / total_frames) * 2 * math.pi) * 0.5 + 0.5
        top_dot_col = PALETTE["MINT"] if pulse_alpha > 0.4 else PALETTE["SHADOW"]
        draw.ellipse([40, 22, 48, 30], fill=top_dot_col)

        # PHASE 1: ASSEMBLY (Frames 0 to 18)
        if f <= 18:
            norm_t = f / 18.0
            for p in particles:
                # Staggered local progression
                adj_t = max(0.0, min(1.0, (norm_t - p["stagger"] * 0.25) / (1.0 - p["stagger"] * 0.25)))
                # Cubic ease-out
                e = 1.0 - math.pow(1.0 - adj_t, 3)

                cur_x = p["sx"] * (1.0 - e) + p["tx"] * e
                cur_y = p["sy"] * (1.0 - e) + p["ty"] * e
                cur_r = max(0.8, p["r"] * e)

                col = p["color"]
                if adj_t < 0.6 and col in (PALETTE["SHADOW"], PALETTE["MID_SHADOW"]):
                    # Dim incoming shadow particles during high-speed transit
                    col = PALETTE["SHADOW"]

                draw.ellipse([cur_x - cur_r, cur_y - cur_r, cur_x + cur_r, cur_y + cur_r], fill=col)

        # PHASE 2: SCANLINE SWEEP (Frames 19 to 27)
        elif 19 <= f <= 27:
            scan_prog = (f - 19) / 8.0
            scan_y = scan_prog * (canvas_size - 40) + 20
            scan_band = 28.0

            # Draw scanline bar
            draw.line([(20, scan_y), (canvas_size - 20, scan_y)], fill=PALETTE["CYAN"], width=2)

            for p in particles:
                cur_x = p["tx"]
                cur_y = p["ty"]
                cur_r = p["r"]
                col = p["color"]

                dist_to_scan = abs(cur_y - scan_y)
                if dist_to_scan < scan_band:
                    # Shimmer highlight
                    shimmer_ratio = 1.0 - (dist_to_scan / scan_band)
                    cur_r = cur_r * (1.0 + 0.35 * shimmer_ratio)
                    if col in (PALETTE["CYAN"], PALETTE["MINT"], PALETTE["WHITE"]):
                        col = PALETTE["WHITE"]
                    elif col == PALETTE["MID_SHADOW"]:
                        col = PALETTE["CYAN"]

                draw.ellipse([cur_x - cur_r, cur_y - cur_r, cur_x + cur_r, cur_y + cur_r], fill=col)

        # PHASE 3: SETTLED STATE (Frames 28 to 35) - Restrained breathing shimmer
        else:
            settled_phase = (f - 28) / 8.0
            pulse_factor = 1.0 + 0.08 * math.sin(settled_phase * 2 * math.pi)
            for p in particles:
                cur_x = p["tx"]
                cur_y = p["ty"]
                cur_r = p["r"]
                if p["color"] in (PALETTE["CYAN"], PALETTE["WHITE"]):
                    cur_r = p["r"] * pulse_factor
                draw.ellipse([cur_x - cur_r, cur_y - cur_r, cur_x + cur_r, cur_y + cur_r], fill=p["color"])

        # Quantize frame using strict adaptive palette (32 colors)
        frame_pal = im.quantize(colors=32, method=Image.Quantize.MEDIANCUT)
        frames.append(frame_pal)

    # Save animated GIF
    frame_duration_ms = int(1000 / fps)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration_ms,
        loop=0,
        optimize=True
    )

    return output_path


# ==============================================================================
# STATIC PNG RENDERER
# ==============================================================================
def generate_static_png(grid, output_path):
    """
    Renders the settled dot-matrix portrait into an ultra-sharp PNG preview.
    """
    grid_size = len(grid)
    canvas_size = 512
    pitch = canvas_size / grid_size

    im = Image.new("RGB", (canvas_size, canvas_size), PALETTE["VOID"])
    draw = ImageDraw.Draw(im)

    # Background frame
    draw.rounded_rectangle([2, 2, canvas_size - 3, canvas_size - 3], radius=18, outline=PALETTE["MID_SHADOW"], width=1)

    # Backplane lines
    for g_pos in range(64, canvas_size, 64):
        draw.line([(g_pos, 8), (g_pos, canvas_size - 8)], fill=PALETTE["DARK_CYANITE"], width=1)
        draw.line([(8, g_pos), (canvas_size - 8, g_pos)], fill=PALETTE["DARK_CYANITE"], width=1)

    # Corner brackets
    draw.line([(16, 36), (16, 16), (36, 16)], fill=PALETTE["CYAN"], width=2)
    draw.line([(canvas_size - 16, 36), (canvas_size - 16, 16), (canvas_size - 36, 16)], fill=PALETTE["CYAN"], width=2)
    draw.line([(16, canvas_size - 36), (16, canvas_size - 16), (36, canvas_size - 16)], fill=PALETTE["CYAN"], width=2)
    draw.line([(canvas_size - 16, canvas_size - 36), (canvas_size - 16, canvas_size - 16), (canvas_size - 36, canvas_size - 16)], fill=PALETTE["CYAN"], width=2)

    # Status node
    draw.ellipse([40, 22, 48, 30], fill=PALETTE["MINT"])

    for y in range(grid_size):
        for x in range(grid_size):
            col = grid[y][x]
            if col == PALETTE["VOID"]:
                continue

            cx = x * pitch + pitch / 2
            cy = y * pitch + pitch / 2

            if col in (PALETTE["SHADOW"], PALETTE["MID_SHADOW"]):
                r = pitch * 0.28
            elif col in (PALETTE["WHITE"], PALETTE["CYAN"]):
                r = pitch * 0.45
            else:
                r = pitch * 0.40

            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    im.save(output_path, "PNG", optimize=True)
    return output_path


# ==============================================================================
# PIPELINE VERIFICATION SUITE
# ==============================================================================
def verify_pipeline_outputs(output_dir):
    """
    Validates all generated assets against Phase 2 requirements:
      - Valid XML structure for SVG
      - Valid GIF decoding and non-zero frames
      - File size limits (SVG < 100 KB, GIF < 1.5 MB)
    """
    out_dir = Path(output_dir)
    svg_path = out_dir / "portrait_dotmatrix.svg"
    gif_path = out_dir / "portrait_assembly.gif"
    png_path = out_dir / "portrait_static.png"

    results = {}

    # 1. SVG Check
    assert svg_path.exists(), f"Missing {svg_path}"
    svg_size = svg_path.stat().st_size
    assert svg_size > 500, f"SVG file suspiciously small: {svg_size} bytes"
    assert svg_size < 100 * 1024, f"SVG exceeds 100KB budget: {svg_size} bytes"
    with open(svg_path, "r", encoding="utf-8") as f:
        ET.fromstring(f.read())
    results["svg"] = {"path": str(svg_path), "size_bytes": svg_size, "valid_xml": True}

    # 2. GIF Check
    assert gif_path.exists(), f"Missing {gif_path}"
    gif_size = gif_path.stat().st_size
    assert gif_size > 10 * 1024, f"GIF file suspiciously small: {gif_size} bytes"
    assert gif_size < 1.5 * 1024 * 1024, f"GIF exceeds 1.5MB budget: {gif_size} bytes"

    gif_im = Image.open(gif_path)
    frame_count = 0
    total_duration_ms = 0
    try:
        while True:
            frame_count += 1
            total_duration_ms += gif_im.info.get("duration", 60)
            gif_im.seek(gif_im.tell() + 1)
    except EOFError:
        pass
    assert frame_count >= 20, f"Expected at least 20 frames in GIF, found {frame_count}"
    assert total_duration_ms >= 1500, f"Expected total duration >= 1.5s, got {total_duration_ms}ms"
    results["gif"] = {
        "path": str(gif_path),
        "size_bytes": gif_size,
        "frames": frame_count,
        "duration_ms": total_duration_ms
    }

    # 3. PNG Check
    assert png_path.exists(), f"Missing {png_path}"
    png_size = png_path.stat().st_size
    png_im = Image.open(png_path)
    assert png_im.size == (512, 512), f"Unexpected PNG size {png_im.size}"
    results["png"] = {"path": str(png_path), "size_bytes": png_size, "dimensions": png_im.size}

    return results


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="TACE-X Dot-Matrix Portrait & Particle-Assembly Generator")
    parser.add_argument("--input", "-i", type=str, default=None, help="Path to input portrait photo (PNG/JPG/WEBP)")
    parser.add_argument("--output-dir", "-o", type=str, default="assets/portrait", help="Destination directory")
    parser.add_argument("--grid-size", "-g", type=int, default=64, help="Grid dimension (default 64)")
    parser.add_argument("--fps", type=int, default=15, help="GIF frame rate (default 15)")
    parser.add_argument("--force-fallback", action="store_true", help="Force synthetic geometric emblem generation")
    parser.add_argument("--test", action="store_true", help="Run validation tests on generated assets")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    is_fallback = False

    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"[!] Warning: Input file '{args.input}' does not exist.")
            print("[*] Defaulting to synthetic TACE-X Cybernetic Architect geometric emblem.")
            grid = generate_cybernetic_architect_grid(grid_size=args.grid_size)
            is_fallback = True
        else:
            try:
                print(f"[*] Processing user-provided portrait: {args.input}")
                grid = process_source_image(args.input, grid_size=args.grid_size)
            except Exception as e:
                print(f"[!] Error reading image '{args.input}': {e}")
                print("[*] Falling back to synthetic TACE-X Cybernetic Architect geometric emblem.")
                grid = generate_cybernetic_architect_grid(grid_size=args.grid_size)
                is_fallback = True
    elif args.force_fallback or True:
        print("[*] No user portrait photo supplied (or --force-fallback specified).")
        print("[*] Synthesizing TACE-X Cybernetic Architect geometric emblem (temporary visual)...")
        grid = generate_cybernetic_architect_grid(grid_size=args.grid_size)
        is_fallback = True

    svg_dest = output_dir / "portrait_dotmatrix.svg"
    gif_dest = output_dir / "portrait_assembly.gif"
    png_dest = output_dir / "portrait_static.png"

    print(f"[*] Generating dot-matrix vector SVG -> {svg_dest}")
    generate_dotmatrix_svg(grid, svg_dest, is_fallback=is_fallback)

    print(f"[*] Generating static PNG preview -> {png_dest}")
    generate_static_png(grid, png_dest)

    print(f"[*] Generating animated particle-assembly GIF (36 frames @ {args.fps} FPS) -> {gif_dest}")
    generate_assembly_gif(grid, gif_dest, fps=args.fps)

    print("[+] All assets generated successfully.")

    if args.test or True:
        print("[*] Verifying output integrity...")
        audit = verify_pipeline_outputs(output_dir)
        print(json.dumps(audit, indent=2))
        print("[✓] Validation passed completely.")

    print("\n[!] TO REGENERATE WITH A PERSONAL PHOTO LATER:")
    print("    python3 scripts/generate_portrait.py --input /path/to/your_headshot.jpg")


if __name__ == "__main__":
    main()
