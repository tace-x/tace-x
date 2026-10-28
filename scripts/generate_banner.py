#!/usr/bin/env python3
"""
TACE-X Signature Animated GitHub README Banner Generator
=========================================================
Generates:
  assets/tace-x-banner.svg

Builds the signature animated identity banner incorporating the user's definitive
falcon emblem silhouette, surrounded by a luminous energy portal, cinematic crystalline
atmosphere, left-aligned typography with verified stack pills, and dynamic telemetry.
"""

import os
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "assets" / "tace-x-banner.svg"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def extract_emblem_svg_paths():
    """Extracts exact RDP-simplified vector paths from the user's master image."""
    src_path = Path("/Users/immanuelmelbin/.gemini/antigravity-ide/brain/99c52b00-68f0-4731-b3a8-364b1d33d0ed/.user_uploaded/media_1793177060989.png")
    im = Image.open(src_path).convert("L")
    arr = (np.array(im) > 120).astype(np.uint8)
    h, w = arr.shape

    visited = np.zeros_like(arr, dtype=bool)
    contours = []
    dirs = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if arr[y, x] and not arr[y, x - 1] and not visited[y, x]:
                contour = []
                start = (y, x)
                curr = start
                dir_idx = 4
                for step in range(50000):
                    contour.append((curr[1], curr[0]))
                    visited[curr[0], curr[1]] = True
                    search_start = (dir_idx + 5) % 8
                    found_next = False
                    for i in range(8):
                        d = (search_start + i) % 8
                        ny = curr[0] + dirs[d][0]
                        nx = curr[1] + dirs[d][1]
                        if 0 <= ny < h and 0 <= nx < w and arr[ny, nx]:
                            curr = (ny, nx)
                            dir_idx = d
                            found_next = True
                            break
                    if not found_next or curr == start:
                        break
                if len(contour) > 50:
                    contours.append(contour)

    def rdp(pts, eps):
        if len(pts) < 3:
            return pts
        pts = np.array(pts, dtype=float)
        start, end = pts[0], pts[-1]
        line_vec = np.array([end[0] - start[0], end[1] - start[1]], dtype=float)
        line_len = np.linalg.norm(line_vec)
        if line_len == 0:
            dists = np.linalg.norm(pts - start, axis=1)
        else:
            line_unit = line_vec / line_len
            norm_vec = np.array([-line_unit[1], line_unit[0]])
            vecs = pts - start
            dists = np.abs(np.dot(vecs, norm_vec))
        max_idx = np.argmax(dists)
        if dists[max_idx] > eps:
            left = rdp(pts[:max_idx + 1], eps)
            right = rdp(pts[max_idx:], eps)
            return np.vstack([left[:-1], right])
        else:
            return np.array([start, end])

    svg_paths = []
    for c in contours:
        simple = rdp(c, 1.2)
        path_d = f"M {simple[0][0]:.1f} {simple[0][1]:.1f} " + " ".join([f"L {p[0]:.1f} {p[1]:.1f}" for p in simple[1:]]) + " Z"
        svg_paths.append(path_d)

    return svg_paths


def build_banner_svg(emblem_paths):
    all_paths_d = " ".join(emblem_paths)

    # Portal center
    PCX = 690
    PCY = 155
    SCALE = 0.222

    svg = f"""<svg width="900" height="320" viewBox="0 0 900 320" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>IMMANUEL MELBIN (@tace-x) — Software · Systems · AI</title>
  <desc>Signature animated developer banner for Immanuel Melbin (@tace-x). Native systems, AI platforms, and high-performance software.</desc>

  <defs>
    <!-- Background Deep Space Gradient -->
    <linearGradient id="bgCanvas" x1="0" y1="0" x2="900" y2="320" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#05080E" />
      <stop offset="45%" stop-color="#03060A" />
      <stop offset="100%" stop-color="#020305" />
    </linearGradient>

    <!-- Top Accent Cyber-Line -->
    <linearGradient id="topLineGradient" x1="0" y1="0" x2="900" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0" />
      <stop offset="25%" stop-color="#00F0FF" stop-opacity="0.8" />
      <stop offset="50%" stop-color="#38BDF8" stop-opacity="1" />
      <stop offset="75%" stop-color="#2563EB" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#00F0FF" stop-opacity="0" />
    </linearGradient>

    <!-- Falcon Emblem Chrome Gradient -->
    <linearGradient id="falconGradient" x1="200" y1="150" x2="850" y2="850" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="22%" stop-color="#E0F7FF" />
      <stop offset="48%" stop-color="#38BDF8" />
      <stop offset="75%" stop-color="#0284C7" />
      <stop offset="100%" stop-color="#1D4ED8" />
    </linearGradient>

    <!-- Energy Sweep Across Emblem -->
    <linearGradient id="energySweepGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0" />
      <stop offset="40%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="60%" stop-color="#38BDF8" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#00F0FF" stop-opacity="0" />
    </linearGradient>

    <!-- Radial Portal Glows -->
    <radialGradient id="portalCoreGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0.38" />
      <stop offset="35%" stop-color="#0284C7" stop-opacity="0.22" />
      <stop offset="70%" stop-color="#1E3A8A" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#05080E" stop-opacity="0" />
    </radialGradient>

    <radialGradient id="portalOuterAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.25" />
      <stop offset="50%" stop-color="#1E40AF" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#020305" stop-opacity="0" />
    </radialGradient>

    <!-- Crystalline Rock Rim Lighting Gradient -->
    <linearGradient id="rockRimGrad" x1="520" y1="240" x2="900" y2="320" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0" />
      <stop offset="15%" stop-color="#00F0FF" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#38BDF8" stop-opacity="0.7" />
      <stop offset="85%" stop-color="#1D4ED8" stop-opacity="0.5" />
      <stop offset="100%" stop-color="#0A0F1D" stop-opacity="0.2" />
    </linearGradient>

    <!-- Progress Meter Beam Gradient -->
    <linearGradient id="meterBeamGrad" x1="0" y1="0" x2="100" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00F0FF" />
      <stop offset="100%" stop-color="#38BDF8" />
    </linearGradient>

    <!-- Filters -->
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16" />
    </filter>
    <filter id="ringGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.5" result="b" />
      <feMerge>
        <feMergeNode in="b" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="emblemFilter" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="b" />
      <feMerge>
        <feMergeNode in="b" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Technical Fine Backplane Grid -->
    <pattern id="hudGrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#FFFFFF" stroke-opacity="0.02" stroke-width="0.75" />
    </pattern>

    <!-- Card Clip -->
    <clipPath id="bannerClip">
      <rect width="900" height="320" rx="16" />
    </clipPath>

    <!-- Falcon Silhouette Clip for Energy Sweep -->
    <clipPath id="falconClip">
      <g transform="translate({PCX}, {PCY}) scale({SCALE}) translate(-518.5, -505.5)">
        <path d="{all_paths_d}" />
      </g>
    </clipPath>
  </defs>

  <style>
    /* CSS Keyframe Animations - 100% SVG and GitHub Camo Compatible */

    /* 1. Portal Aura Breathing */
    .portal-aura-core {{
      animation: auraPulse 4.6s ease-in-out infinite;
      transform-origin: {PCX}px {PCY}px;
    }}
    .portal-aura-outer {{
      animation: auraOuter 6.4s ease-in-out infinite alternate;
      transform-origin: {PCX}px {PCY}px;
    }}
    @keyframes auraPulse {{
      0%, 100% {{ transform: scale(0.94); opacity: 0.78; }}
      50% {{ transform: scale(1.06); opacity: 1; }}
    }}
    @keyframes auraOuter {{
      0% {{ transform: scale(0.92); opacity: 0.65; }}
      100% {{ transform: scale(1.10); opacity: 0.95; }}
    }}

    /* 2. Portal Energy Ring Rotation */
    .portal-ring {{
      animation: ringSpin 16s linear infinite;
      transform-origin: {PCX}px {PCY}px;
    }}
    .portal-ring-reverse {{
      animation: ringSpinRev 22s linear infinite;
      transform-origin: {PCX}px {PCY}px;
    }}
    @keyframes ringSpin {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    @keyframes ringSpinRev {{
      from {{ transform: rotate(360deg); }}
      to {{ transform: rotate(0deg); }}
    }}

    /* 3. Energy Sweep Across Falcon Emblem */
    .energy-sweep {{
      animation: energySweep 4.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }}
    @keyframes energySweep {{
      0% {{ transform: translateX(-280px) rotate(20deg); opacity: 0; }}
      12% {{ opacity: 0.9; }}
      45% {{ opacity: 0.95; }}
      58% {{ transform: translateX(380px) rotate(20deg); opacity: 0; }}
      100% {{ transform: translateX(380px) rotate(20deg); opacity: 0; }}
    }}

    /* 4. Drifting Particles Field */
    .pt1 {{ animation: pDrift1 5.4s ease-in-out infinite; }}
    .pt2 {{ animation: pDrift2 6.8s ease-in-out infinite 0.9s; }}
    .pt3 {{ animation: pDrift1 5.9s ease-in-out infinite 1.8s; }}
    .pt4 {{ animation: pDrift2 7.2s ease-in-out infinite 2.7s; }}
    .pt5 {{ animation: pDrift1 6.5s ease-in-out infinite 3.6s; }}

    @keyframes pDrift1 {{
      0%, 100% {{ transform: translate(0, 0); opacity: 0.3; }}
      50% {{ transform: translate(14px, -16px); opacity: 0.95; }}
    }}
    @keyframes pDrift2 {{
      0%, 100% {{ transform: translate(0, 0); opacity: 0.35; }}
      50% {{ transform: translate(-12px, 14px); opacity: 0.9; }}
    }}

    /* 5. Crystalline Energy Pulse */
    .rock-pulse {{
      animation: rockGlow 5.2s ease-in-out infinite alternate;
    }}
    @keyframes rockGlow {{
      0% {{ opacity: 0.75; }}
      100% {{ opacity: 1; filter: drop-shadow(0 0 10px rgba(0, 240, 255, 0.45)); }}
    }}

    /* 6. Name Heading Shimmer */
    .name-shimmer {{
      animation: nameGlow 6s ease-in-out infinite;
    }}
    @keyframes nameGlow {{
      0%, 75%, 100% {{ opacity: 0.96; }}
      88% {{ opacity: 1; filter: drop-shadow(0 0 8px rgba(0, 240, 255, 0.4)); }}
    }}

    /* 7. Progress Meter Sweep */
    .meter-bar {{
      animation: meterFlow 3.2s ease-in-out infinite alternate;
    }}
    @keyframes meterFlow {{
      0% {{ width: 22px; }}
      100% {{ width: 44px; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      *, .portal-aura-core, .portal-aura-outer, .portal-ring, .portal-ring-reverse,
      .energy-sweep, .pt1, .pt2, .pt3, .pt4, .pt5, .rock-pulse, .name-shimmer, .meter-bar {{
        animation: none !important;
      }}
    }}
  </style>

  <!-- === BASE CONTAINER === -->
  <rect width="900" height="320" rx="16" fill="url(#bgCanvas)" stroke="#172338" stroke-width="1.5" />

  <g clip-path="url(#bannerClip)">
    <!-- Backplane Technical HUD Grid -->
    <rect width="900" height="320" fill="url(#hudGrid)" />

    <!-- Top Status Line -->
    <line x1="0" y1="34" x2="900" y2="34" stroke="url(#topLineGradient)" stroke-width="1" />
    <text x="56" y="22" fill="#38BDF8" font-family="'JetBrains Mono', 'SF Mono', Consolas, monospace" font-size="9.5" font-weight="700" letter-spacing="2">TACE-X // SYSTEMS ONLINE</text>
    <text x="844" y="22" text-anchor="end" fill="#475569" font-family="'JetBrains Mono', 'SF Mono', Consolas, monospace" font-size="9" letter-spacing="1.5">GITHUB.COM/TACE-X</text>

    <!-- === RIGHT SIDE: CINEMATIC CRYSTALLINE PORTAL & EMBLEM === -->
    <!-- Ambient Radial Glows -->
    <ellipse cx="{PCX}" cy="{PCY}" rx="190" ry="135" fill="url(#portalOuterAura)" filter="url(#softGlow)" class="portal-aura-outer" />
    <circle cx="{PCX}" cy="{PCY}" r="105" fill="url(#portalCoreGlow)" filter="url(#softGlow)" class="portal-aura-core" />

    <!-- Circular Portal Energy Rings -->
    <g class="portal-ring" filter="url(#ringGlow)">
      <circle cx="{PCX}" cy="{PCY}" r="105" fill="none" stroke="#00F0FF" stroke-opacity="0.6" stroke-width="1.8" stroke-dasharray="75 22 140 18 45 28" />
      <circle cx="{PCX}" cy="{PCY}" r="113" fill="none" stroke="#38BDF8" stroke-opacity="0.35" stroke-width="1" stroke-dasharray="18 40 85 30" />
    </g>
    <g class="portal-ring-reverse">
      <circle cx="{PCX}" cy="{PCY}" r="117" fill="none" stroke="#1D4ED8" stroke-opacity="0.45" stroke-width="1.2" stroke-dasharray="40 50 110 35" />
    </g>

    <!-- Crystalline Rocky Terrain Silhouette & Neon Rim (Bottom Right) -->
    <g class="rock-pulse">
      <path d="M 520 320 L 550 292 L 580 300 L 610 274 L 640 288 L 670 262 L 705 282 L 735 258 L 770 280 L 810 260 L 850 282 L 880 266 L 900 278 L 900 320 Z" fill="#060A14" />
      <path d="M 520 320 L 550 292 L 580 300 L 610 274 L 640 288 L 670 262 L 705 282 L 735 258 L 770 280 L 810 260 L 850 282 L 880 266 L 900 278" fill="none" stroke="url(#rockRimGrad)" stroke-width="1.8" filter="url(#ringGlow)" />
    </g>

    <!-- THE DEFINITIVE FALCON EMBLEM (USER MASTER ASSET) -->
    <g id="tace-x-falcon" filter="url(#emblemFilter)">
      <g transform="translate({PCX}, {PCY}) scale({SCALE}) translate(-518.5, -505.5)">
""" + "\n".join([f'        <path d="{p}" fill="url(#falconGradient)" />' for p in emblem_paths]) + f"""
      </g>
    </g>

    <!-- Energy Sweep Across Emblem -->
    <g clip-path="url(#falconClip)">
      <rect x="570" y="40" width="70" height="230" fill="url(#energySweepGrad)" class="energy-sweep" />
    </g>

    <!-- Drifting Floating Energy Micro-Particles -->
    <g id="portal-particles">
      <circle cx="620" cy="115" r="1.8" fill="#FFFFFF" class="pt1" filter="url(#emblemFilter)" />
      <circle cx="760" cy="95" r="2.2" fill="#00F0FF" class="pt2" filter="url(#emblemFilter)" />
      <circle cx="780" cy="180" r="1.6" fill="#38BDF8" class="pt3" filter="url(#emblemFilter)" />
      <circle cx="615" cy="215" r="1.9" fill="#00F0FF" class="pt4" filter="url(#emblemFilter)" />
      <circle cx="670" cy="70" r="2.0" fill="#FFFFFF" class="pt5" filter="url(#emblemFilter)" />
      <circle cx="750" cy="225" r="1.4" fill="#38BDF8" class="pt2" />
      <circle cx="595" cy="160" r="1.5" fill="#00F0FF" class="pt1" />
    </g>

    <!-- Far Right HUD Telemetry Column -->
    <g transform="translate(820, 72)" opacity="0.65">
      <text x="0" y="0" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" letter-spacing="1.5">LEARN</text>
      <text x="0" y="14" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" letter-spacing="1.5">BUILD</text>
      <text x="0" y="28" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" letter-spacing="1.5">AUTOMATE</text>
      <text x="0" y="42" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" letter-spacing="1.5">CREATE</text>
      <text x="0" y="56" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" letter-spacing="1.5">IMPACT</text>
    </g>

    <g transform="translate(820, 182)" opacity="0.55">
      <text x="0" y="0" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="8" letter-spacing="1">&lt;/&gt; CODE</text>
      <text x="0" y="14" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="8" letter-spacing="1">⛶ SYSTEMS</text>
      <text x="0" y="28" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="8" letter-spacing="1">△ AI</text>
      <text x="0" y="42" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="8" letter-spacing="1">▷ AUTOMATION</text>
      <text x="0" y="56" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="8" letter-spacing="1">◯ REAL-WORLD</text>
    </g>

    <!-- === LEFT SIDE: TYPOGRAPHY & IDENTITY === -->
    <!-- Small Eyebrow -->
    <g transform="translate(56, 86)">
      <rect x="0" y="-10" width="5" height="5" fill="#00F0FF" />
      <text x="14" y="-5" fill="#00F0FF" font-family="'JetBrains Mono', 'SF Mono', Consolas, monospace" font-size="11" font-weight="700" letter-spacing="2.6">TACE-X  //  SOFTWARE • SYSTEMS • AI</text>
    </g>

    <!-- Main Heading -->
    <text x="56" y="146" fill="#F8FAFC" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, sans-serif" font-size="44" font-weight="900" letter-spacing="0.5" class="name-shimmer">IMMANUEL MELBIN</text>

    <!-- Handle & Accent Bar -->
    <g transform="translate(56, 178)">
      <text x="0" y="0" fill="#00F0FF" font-family="'JetBrains Mono', 'SF Mono', Consolas, monospace" font-size="14.5" font-weight="700" letter-spacing="1.2">@tace-x</text>
      <line x1="72" y1="-5" x2="114" y2="-5" stroke="#00F0FF" stroke-width="2" stroke-linecap="round" filter="url(#ringGlow)" />
    </g>

    <!-- Short Description -->
    <text x="56" y="212" fill="#94A3B8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, sans-serif" font-size="12" font-weight="400" letter-spacing="0.4">BUILDING NATIVE SYSTEMS, AI PLATFORMS, AND HIGH-PERFORMANCE SOFTWARE.</text>

    <!-- Verified Technology Badges -->
    <g transform="translate(56, 240)">
      <!-- Rust -->
      <rect x="0" y="0" width="56" height="20" rx="10" fill="#0B1322" stroke="#F59E0B" stroke-width="1" />
      <text x="28" y="13.5" text-anchor="middle" fill="#F59E0B" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="9.5" font-weight="600">Rust</text>

      <!-- TypeScript -->
      <rect x="64" y="0" width="84" height="20" rx="10" fill="#0B1322" stroke="#38BDF8" stroke-width="1" />
      <text x="106" y="13.5" text-anchor="middle" fill="#38BDF8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="9.5" font-weight="600">TypeScript</text>

      <!-- React -->
      <rect x="156" y="0" width="60" height="20" rx="10" fill="#0B1322" stroke="#00F0FF" stroke-width="1" />
      <text x="186" y="13.5" text-anchor="middle" fill="#00F0FF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="9.5" font-weight="600">React</text>

      <!-- AI / ML -->
      <rect x="224" y="0" width="68" height="20" rx="10" fill="#0B1322" stroke="#10B981" stroke-width="1" />
      <text x="258" y="13.5" text-anchor="middle" fill="#10B981" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="9.5" font-weight="600">AI / ML</text>

      <!-- Firebase -->
      <rect x="300" y="0" width="72" height="20" rx="10" fill="#0B1322" stroke="#F97316" stroke-width="1" />
      <text x="336" y="13.5" text-anchor="middle" fill="#F97316" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="9.5" font-weight="600">Firebase</text>
    </g>

    <!-- Bottom Telemetry Progress Meter -->
    <g transform="translate(56, 286)">
      <text x="0" y="0" fill="#38BDF8" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700">//</text>
      <rect x="22" y="-9" width="55" height="4" rx="2" fill="#17253D" />
      <rect x="22" y="-9" width="32" height="4" rx="2" fill="url(#meterBeamGrad)" class="meter-bar" />
      <text x="92" y="0" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="9.5" font-weight="600" letter-spacing="1.5">IDEAS  →  SYSTEMS  →  IMPACT</text>
    </g>

    <!-- Technical Reticles (Corners) -->
    <path d="M 22 52 L 22 42 L 32 42" fill="none" stroke="#253550" stroke-width="1.2" />
    <path d="M 878 52 L 878 42 L 868 42" fill="none" stroke="#253550" stroke-width="1.2" />
    <path d="M 22 288 L 22 298 L 32 298" fill="none" stroke="#253550" stroke-width="1.2" />
    <path d="M 878 288 L 878 298 L 868 298" fill="none" stroke="#253550" stroke-width="1.2" />
  </g>
</svg>
"""
    return svg


def render_preview(svg_path, png_path):
    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--window-size=900,320",
        "--default-background-color=020305",
        f"--screenshot={str(png_path)}",
        str(svg_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def validate_svg(svg_content):
    root = ET.fromstring(svg_content)
    assert root.tag.endswith("svg"), f"Root tag is not svg: {root.tag}"
    assert root.attrib.get("viewBox") == "0 0 900 320", f"Unexpected viewBox: {root.attrib.get('viewBox')}"
    size_kb = len(svg_content.encode("utf-8")) / 1024
    assert size_kb < 150, f"SVG exceeds 150 KB budget: {size_kb:.1f} KB"
    print(f"  ✓ Valid XML, viewBox='0 0 900 320', size={size_kb:.1f} KB (< 150 KB budget)")


def main():
    print("[*] Extracting definitive falcon vector contours from user upload...")
    paths = extract_emblem_svg_paths()
    print(f"  ✓ Extracted {len(paths)} vector silhouette contours.")

    print("[*] Generating cinematic animated banner SVG...")
    svg_code = build_banner_svg(paths)
    validate_svg(svg_code)

    OUTPUT_PATH.write_text(svg_code, encoding="utf-8")
    print(f"  ✓ Written to {OUTPUT_PATH.relative_to(REPO_ROOT)}")

    preview_png = REPO_ROOT / "assets" / "tace-x-banner-preview.png"
    render_preview(OUTPUT_PATH, preview_png)
    print(f"  ✓ Rendered test preview to {preview_png.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
