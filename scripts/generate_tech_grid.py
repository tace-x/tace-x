#!/usr/bin/env python3
"""
TACE-X Engineering Arsenal Technology Grid Generator
=====================================================
Generates:
  assets/tech-grid.svg (and mirrors to assets/tech-strip.svg for backward compatibility)

Displays the 13 requested technologies in a prominent, responsive 4-column grid:
  1. HTML
  2. CSS
  3. JavaScript
  4. TypeScript
  5. Python
  6. Java
  7. Rust
  8. React
  9. Node.js
  10. Tailwind CSS
  11. Vite
  12. Firebase
  13. Git

Design:
  - Dark, premium container with subtle borders and cyan accents.
  - 4 columns on desktop, wrapping naturally.
  - Large (24x24) official vector logos in a horizontal logo-and-text arrangement.
  - Perfectly aligned spacing, typography, and accessible titles.
"""

from pathlib import Path
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "assets" / "tech-grid.svg"
LEGACY_FILE = REPO_ROOT / "assets" / "tech-strip.svg"

TECHS = [
    {
        "id": "html",
        "name": "HTML",
        "accent": "#F97316",
        # 24x24 HTML5 Shield
        "icon": """
          <g transform="translate(-12, -12)">
            <path d="M4 2l1.6 18 6.4 1.8 6.4-1.8L20 2H4z" fill="#F97316" fill-opacity="0.15" stroke="#F97316" stroke-width="1.2"/>
            <path d="M12 4v16.1l4.8-1.3 1.3-14.8H12z" fill="#F97316" fill-opacity="0.3"/>
            <!-- 5 numeral cutout -->
            <path d="M7 6h10l-.3 3.2H10.5l.2 2.6H16.3l-.6 6.4-3.7 1-3.7-1-.3-3H10.2l.1 1.4 1.7.5 1.7-.5.3-3.1H7.4L7 6z" fill="#F8FAFC"/>
          </g>
        """
    },
    {
        "id": "css",
        "name": "CSS",
        "accent": "#38BDF8",
        # 24x24 CSS3 Shield
        "icon": """
          <g transform="translate(-12, -12)">
            <path d="M4 2l1.6 18 6.4 1.8 6.4-1.8L20 2H4z" fill="#38BDF8" fill-opacity="0.15" stroke="#38BDF8" stroke-width="1.2"/>
            <path d="M12 4v16.1l4.8-1.3 1.3-14.8H12z" fill="#38BDF8" fill-opacity="0.3"/>
            <!-- 3 numeral cutout -->
            <path d="M7 6h10l-.9 9.8-4.1 1.1-4.1-1.1-.3-3h2.1l.1 1.4 2.2.6 2.2-.6.4-4H8.8l-.3-3H16l.3-2.8H7V6z" fill="#F8FAFC"/>
          </g>
        """
    },
    {
        "id": "javascript",
        "name": "JavaScript",
        "accent": "#F59E0B",
        # 24x24 JS Square
        "icon": """
          <g transform="translate(-12, -12)">
            <rect x="2" y="2" width="20" height="20" rx="4" fill="#F59E0B" fill-opacity="0.15" stroke="#F59E0B" stroke-width="1.2"/>
            <!-- JS Monogram -->
            <path d="M8.5 9v7.5c0 1.8-1 2.5-2.5 2.5-1 0-1.8-.4-2.2-1l1.2-1.4c.3.3.6.5 1 .5.5 0 .8-.3.8-1V9h1.7z" fill="#F8FAFC"/>
            <path d="M18.5 11.2c-.4-.6-1.1-.9-2-.9-1.2 0-2 .7-2 1.6 0 1 .6 1.4 1.8 1.8 1.3.4 2.4.9 2.4 2.4 0 1.6-1.3 2.5-2.9 2.5-1.2 0-2.2-.4-2.9-1.2l1.1-1.6c.5.5 1.1.9 1.8.9.8 0 1.3-.4 1.3-.9 0-.6-.5-.9-1.7-1.4-1.5-.5-2.5-1.1-2.5-2.3 0-1.5 1.2-2.5 2.9-2.5 1 0 1.9.3 2.6.9l-1 1.7z" fill="#F59E0B"/>
          </g>
        """
    },
    {
        "id": "typescript",
        "name": "TypeScript",
        "accent": "#00F0FF",
        # 24x24 TS Square
        "icon": """
          <g transform="translate(-12, -12)">
            <rect x="2" y="2" width="20" height="20" rx="4" fill="#00F0FF" fill-opacity="0.12" stroke="#00F0FF" stroke-width="1.2"/>
            <!-- T -->
            <path d="M5.5 8h7v1.8H10v7.2H7.8V9.8H5.5V8z" fill="#94A3B8"/>
            <!-- S -->
            <path d="M19 10.2c-.4-.6-1.1-.9-2-.9-1.2 0-2 .7-2 1.6 0 1 .6 1.4 1.8 1.8 1.3.4 2.4.9 2.4 2.4 0 1.6-1.3 2.5-2.9 2.5-1.2 0-2.2-.4-2.9-1.2l1.1-1.6c.5.5 1.1.9 1.8.9.8 0 1.3-.4 1.3-.9 0-.6-.5-.9-1.7-1.4-1.5-.5-2.5-1.1-2.5-2.3 0-1.5 1.2-2.5 2.9-2.5 1 0 1.9.3 2.6.9l-1 1.7z" fill="#00F0FF"/>
          </g>
        """
    },
    {
        "id": "python",
        "name": "Python",
        "accent": "#38BDF8",
        # 24x24 Python Dual Snakes
        "icon": """
          <g transform="translate(-12, -12)">
            <!-- Top snake -->
            <path d="M11.8 2c-3.5 0-3.3 1.5-3.3 1.5l.01 1.6h3.3v.5H6c0 0-2.3.3-2.3 3.3s1.9 3.1 1.9 3.1h1.1V10.4c0-1.9 1.6-1.9 1.6-1.9h3.3c1.6 0 1.6-1.5 1.6-1.5V3.9S13.4 2 11.8 2zm-.9 1a.6.6 0 1 1 0 1.2.6.6 0 0 1 0-1.2z" fill="#38BDF8"/>
            <!-- Bottom snake -->
            <path d="M12.2 22c3.5 0 3.3-1.5 3.3-1.5l-.01-1.6h-3.3v-.5H18c0 0 2.3-.3 2.3-3.3s-1.9-3.1-1.9-3.1h-1.1v1.6c0 1.9-1.6 1.9-1.6 1.9H12.4c-1.6 0-1.6 1.5-1.6 1.5v3.6s-.2 1.9 1.4 1.9zm.9-1a.6.6 0 1 1 0-1.2.6.6 0 0 1 0 1.2z" fill="#F59E0B"/>
          </g>
        """
    },
    {
        "id": "java",
        "name": "Java",
        "accent": "#F43F5E",
        # 24x24 Java Coffee Cup & Vapors
        "icon": """
          <g transform="translate(-12, -12)">
            <!-- Vapors -->
            <path d="M10 2.5c1 1.5-1 2.5 0 4" fill="none" stroke="#F43F5E" stroke-width="1.2" stroke-linecap="round"/>
            <path d="M13 2c1 1.8-1 3 0 4.5" fill="none" stroke="#F59E0B" stroke-width="1.2" stroke-linecap="round"/>
            <path d="M16 3c1 1.2-1 2 0 3.5" fill="none" stroke="#F43F5E" stroke-width="1.2" stroke-linecap="round"/>
            <!-- Cup & Saucer -->
            <path d="M6 10h11v5c0 2.2-1.8 4-4 4H10c-2.2 0-4-1.8-4-4v-5z" fill="#F43F5E" fill-opacity="0.18" stroke="#F43F5E" stroke-width="1.2"/>
            <path d="M17 11.5h1.5a2 2 0 0 1 0 4H17" fill="none" stroke="#F43F5E" stroke-width="1.2"/>
            <path d="M4.5 20.5h15" stroke="#94A3B8" stroke-width="1.2" stroke-linecap="round"/>
          </g>
        """
    },
    {
        "id": "rust",
        "name": "Rust",
        "accent": "#FB923C",
        # 24x24 Rust Cog & R
        "icon": """
          <g transform="translate(-12, -12)">
            <path d="M11 2h2l.5 2.5c.6.2 1.2.5 1.8.9l2.3-1.3 1.7 1.7-1.3 2.3c.4.6.7 1.2.9 1.8L21.4 11v2l-2.5.5c-.2.6-.5 1.2-.9 1.8l1.3 2.3-1.7 1.7-2.3-1.3c-.6.4-1.2.7-1.8.9l-.5 2.5h-2l-.5-2.5c-.6-.2-1.2-.5-1.8-.9l-2.3 1.3-1.7-1.7 1.3-2.3c-.4-.6-.7-1.2-.9-1.8L2.6 13v-2l2.5-.5c.2-.6.5-1.2.9-1.8L4.7 6.4l1.7-1.7 2.3 1.3c.6-.4 1.2-.7 1.8-.9L11 2z" fill="#070A0F" stroke="#FB923C" stroke-width="1.2"/>
            <circle cx="12" cy="12" r="5" fill="#0B111E" stroke="#00F0FF" stroke-width="1"/>
            <!-- R -->
            <path d="M10 9h2.6c1 0 1.6.5 1.6 1.3 0 .7-.5 1.2-1.2 1.3l1.4 3.4h-1.3l-1.2-3.1h-.6v3.1H10V9zm1.3 2.1h1.2c.4 0 .6-.2.6-.6s-.2-.6-.6-.6h-1.2v1.2z" fill="#F8FAFC"/>
          </g>
        """
    },
    {
        "id": "react",
        "name": "React",
        "accent": "#00F0FF",
        # 24x24 React Atom
        "icon": """
          <g transform="translate(-12, -12)">
            <circle cx="12" cy="12" r="2.2" fill="#00F0FF"/>
            <ellipse cx="12" cy="12" rx="9.5" ry="3.8" fill="none" stroke="#00F0FF" stroke-width="1.1"/>
            <ellipse cx="12" cy="12" rx="9.5" ry="3.8" fill="none" stroke="#38BDF8" stroke-width="1.1" transform="rotate(60 12 12)"/>
            <ellipse cx="12" cy="12" rx="9.5" ry="3.8" fill="none" stroke="#818CF8" stroke-width="1.1" transform="rotate(120 12 12)"/>
          </g>
        """
    },
    {
        "id": "nodejs",
        "name": "Node.js",
        "accent": "#10B981",
        # 24x24 Node Hexagon & N
        "icon": """
          <g transform="translate(-12, -12)">
            <path d="M12 2l8.5 4.8v9.6L12 21.2 3.5 16.4V6.8L12 2z" fill="#071A12" stroke="#10B981" stroke-width="1.2"/>
            <!-- N glyph -->
            <path d="M8.5 7.5v8.5l7-4V3.5l-7 4zm1.8 2.6l3.6-2v5.4l-3.6 2.1V10.1z" fill="#F8FAFC"/>
          </g>
        """
    },
    {
        "id": "tailwind",
        "name": "Tailwind CSS",
        "accent": "#00F0FF",
        # 24x24 Tailwind Twin Waves
        "icon": """
          <g transform="translate(-12, -12)">
            <path d="M6.5 10c1.2-2.4 3-3.4 5-2.8 1.6.5 2.4 1.6 3.4 2.6 1.1 1.2 2.3 2.5 4.6 2.5 2 0 3.4-1.2 4.2-3.4-1.1.9-2.3 1.2-3.5.7-1.3-.5-2.2-1.6-3.1-2.6-1.1-1.2-2.3-2.5-4.6-2.5-2.2 0-3.6 1.2-4.3 3.4l-1.7 2.1z" fill="#00F0FF"/>
            <path d="M2 16c1.2-2.4 3-3.4 5-2.8 1.6.5 2.4 1.6 3.4 2.6 1.1 1.2 2.3 2.5 4.6 2.5 2 0 3.4-1.2 4.2-3.4-1.1.9-2.3 1.2-3.5.7-1.3-.5-2.2-1.6-3.1-2.6-1.1-1.2-2.3-2.5-4.6-2.5-2.2 0-3.6 1.2-4.3 3.4L2 16z" fill="#38BDF8"/>
          </g>
        """
    },
    {
        "id": "vite",
        "name": "Vite",
        "accent": "#8B5CF6",
        # 24x24 Vite V-Shield & Bolt
        "icon": """
          <g transform="translate(-12, -12)">
            <path d="M21 4.5L12 21.5 3 4.5h18z" fill="#140D2E" stroke="#8B5CF6" stroke-width="1.2"/>
            <!-- Lightning -->
            <path d="M15 3.5L8.5 13H13l-2 7 7-10.5h-4.5l1.5-6z" fill="#00F0FF"/>
          </g>
        """
    },
    {
        "id": "firebase",
        "name": "Firebase",
        "accent": "#F59E0B",
        # 24x24 Firebase Flame
        "icon": """
          <g transform="translate(-12, -12)">
            <path d="M4.5 17.5L7.2 5c.1-.5.7-.6 1-.2l3.1 4.3L4.5 17.5z" fill="#F59E0B" fill-opacity="0.8"/>
            <path d="M4.5 17.5l15.6-3.4L14.4 2.8c-.2-.5-1-.5-1.1 0L4.5 17.5z" fill="#F59E0B"/>
            <path d="M20.1 14.1l-2.8-5.2c-.2-.4-.7-.5-1-.1L4.5 17.5l11.4 2.8c.8.2 1.7-.2 1.9-1l2.3-5.2z" fill="#00F0FF"/>
          </g>
        """
    },
    {
        "id": "git",
        "name": "Git",
        "accent": "#F43F5E",
        # 24x24 Git Rhombus & Branching Nodes
        "icon": """
          <g transform="translate(-12, -12)">
            <rect x="3.5" y="3.5" width="17" height="17" rx="3" fill="#1C0E0B" stroke="#F43F5E" stroke-width="1.2" transform="rotate(45 12 12)"/>
            <circle cx="8" cy="16" r="1.8" fill="#00F0FF"/>
            <circle cx="16" cy="8" r="1.8" fill="#F8FAFC"/>
            <circle cx="16" cy="16" r="1.8" fill="#F8FAFC"/>
            <path d="M8 16h4.5a3.5 3.5 0 0 0 3.5-3.5V8" fill="none" stroke="#00F0FF" stroke-width="1.2"/>
            <line x1="16" y1="16" x2="16" y2="12" stroke="#F8FAFC" stroke-width="1.2"/>
          </g>
        """
    }
]

def generate_svg():
    width = 860
    height = 296

    # 4-column responsive grid layout:
    # Row 0: HTML, CSS, JavaScript, TypeScript (4 items)
    # Row 1: Python, Java, Rust, React (4 items)
    # Row 2: Node.js, Tailwind CSS, Vite, Firebase (4 items)
    # Row 3: Git (1 item centered across bottom)
    card_w = 196
    card_h = 46
    gap_x = 13
    gap_y = 10

    cards_svg = []
    for idx, t in enumerate(TECHS):
        if idx < 12:
            row = idx // 4
            col = idx % 4
            x = 19 + col * (card_w + gap_x)
            y = 58 + row * (card_h + gap_y)
            w = card_w
        else:
            # Row 3: Git centered
            w = 230
            x = (width - w) // 2
            y = 58 + 3 * (card_h + gap_y)

        icon_cx = x + 24
        icon_cy = y + card_h // 2
        text_x = x + 48
        text_y = y + card_h // 2 + 4

        card = f"""
    <!-- Card: {t['name']} -->
    <g id="tech-{t['id']}">
      <title>{t['name']}</title>
      <rect x="{x}" y="{y}" width="{w}" height="{card_h}" rx="8" fill="#0B111E" stroke="#1E293B" stroke-width="1"/>
      <!-- Accent Indicator Bar -->
      <path d="M{x+1} {y+10}v{card_h-20}" stroke="{t['accent']}" stroke-width="2.5" stroke-linecap="round"/>
      <!-- Icon (24x24) -->
      <g transform="translate({icon_cx}, {icon_cy})">
        {t['icon']}
      </g>
      <!-- Label -->
      <text x="{text_x}" y="{text_y}" fill="#F8FAFC" font-family="'JetBrains Mono', -apple-system, monospace" font-size="12" font-weight="700" letter-spacing="0.5">{t['name']}</text>
    </g>"""
        cards_svg.append(card)

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>ENGINEERING ARSENAL — 13 Technologies · One Builder · Built to Ship</title>
  <desc>TACE-X Core Technology Toolkit: HTML, CSS, JavaScript, TypeScript, Python, Java, Rust, React, Node.js, Tailwind CSS, Vite, Firebase, Git</desc>

  <defs>
    <linearGradient id="headerLine" x1="20" y1="0" x2="{width-20}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="#38BDF8" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#818CF8" stop-opacity="0.4"/>
    </linearGradient>
  </defs>

  <!-- Container Box -->
  <rect width="{width}" height="{height}" rx="12" fill="#070A0F" stroke="#1E293B" stroke-width="1.2"/>
  <line x1="20" y1="1" x2="{width - 20}" y2="1" stroke="url(#headerLine)" stroke-width="1"/>

  <!-- Top Header Inside Graphic -->
  <g transform="translate(24, 28)">
    <!-- Cyan pip -->
    <circle cx="6" cy="6" r="3.5" fill="#00F0FF"/>
    <text x="18" y="10" fill="#F8FAFC" font-family="'JetBrains Mono', -apple-system, monospace" font-size="13" font-weight="800" letter-spacing="1.5">ENGINEERING ARSENAL</text>
    <text x="{width - 48}" y="10" text-anchor="end" fill="#64748B" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" letter-spacing="1">13 TECHNOLOGIES · ONE BUILDER · BUILT TO SHIP</text>
  </g>
  <line x1="20" y1="46" x2="{width - 20}" y2="46" stroke="#1E293B" stroke-width="1"/>

  <!-- 13 Technology Cards (4-Column Layout) -->
  {''.join(cards_svg)}
</svg>
"""

    OUTPUT_FILE.write_text(svg_content, encoding="utf-8")
    # Also mirror to LEGACY_FILE so any cached/external or test links resolve
    LEGACY_FILE.write_text(svg_content, encoding="utf-8")
    print(f"[✓] Generated Engineering Arsenal -> {OUTPUT_FILE} and {LEGACY_FILE} (13 technologies)")

if __name__ == "__main__":
    generate_svg()
