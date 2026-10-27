#!/usr/bin/env python3
"""
Generate compact project card SVGs for the 3 selected showcase projects.
Cards are minimal: project name, 1 sentence, language tag, repo link.
"""
import os
from pathlib import Path

PALETTE = {
    "VOID":    "#0B0F17",
    "DARK":    "#070A0F",
    "SHADOW":  "#111C2D",
    "MID":     "#1E293B",
    "CYAN":    "#00F0FF",
    "CYAN_D":  "#38BDF8",
    "MINT":    "#10B981",
    "VIOLET":  "#8B5CF6",
    "AMBER":   "#F59E0B",
    "WHITE":   "#F8FAFC",
    "MUTED":   "#94A3B8",
    "SLATE":   "#64748B",
}

PROJECTS = [
    {
        "id":    "terminalvision",
        "name":  "TerminalVision",
        "tag":   "NATIVE SYSTEMS",
        "tag_color": PALETTE["MINT"],
        "desc":  "High-performance native Rust terminal file manager with live Unix PTY, dual-pane navigation, and in-process Git analytics.",
        "url":   "https://github.com/tace-x/TerminalVision",
        "lang":  "Rust  ·  Unix PTY  ·  Ratatui",
        "lang_color": PALETTE["AMBER"],
        "accent": PALETTE["MINT"],
    },
    {
        "id":    "nocap",
        "name":  "NO CAP",
        "tag":   "AI VERIFICATION",
        "tag_color": PALETTE["VIOLET"],
        "desc":  "AI-powered rumour intelligence desk — dissects viral claims, computes credibility scores via NVIDIA NIM + Gemma 4.",
        "url":   "https://github.com/tace-x/NOCAP",
        "lang":  "TypeScript  ·  React 19  ·  NVIDIA NIM",
        "lang_color": PALETTE["VIOLET"],
        "accent": PALETTE["VIOLET"],
    },
    {
        "id":    "capcam",
        "name":  "CAPCAM",
        "tag":   "BROWSER SYSTEMS",
        "tag_color": PALETTE["CYAN"],
        "desc":  "Chrome MV3 extension that intercepts WebRTC camera tracks via an offscreen canvas pipeline — zero cloud, local-first.",
        "url":   "https://github.com/tace-x/CAPCAM",
        "lang":  "TypeScript  ·  Chrome MV3  ·  WebRTC",
        "lang_color": PALETTE["CYAN_D"],
        "accent": PALETTE["CYAN"],
    },
]

CARD_W = 860
CARD_H = 110


def escape(text):
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def generate_card(project, output_path):
    acc = project["accent"]
    tag_col = project["tag_color"]
    lang_col = project["lang_color"]

    name_len = len(project["name"]) * 14 + 40
    tag_len  = len(project["tag"]) * 7.5 + 20

    svg = f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>{escape(project["name"])} — TACE-X</title>
  <desc>{escape(project["desc"])}</desc>
  <defs>
    <linearGradient id="bg_{project["id"]}" x1="0" y1="0" x2="{CARD_W}" y2="{CARD_H}" gradientUnits="userSpaceOnUse">
      <stop stop-color="{PALETTE["DARK"]}"/>
      <stop offset="1" stop-color="{PALETTE["VOID"]}"/>
    </linearGradient>
  </defs>

  <!-- Card background -->
  <rect width="{CARD_W}" height="{CARD_H}" rx="10" fill="url(#bg_{project["id"]})" stroke="{PALETTE["MID"]}" stroke-width="1.2"/>

  <!-- Left accent bar -->
  <rect x="0" y="0" width="4" height="{CARD_H}" rx="2" fill="{acc}"/>

  <!-- Tag pill -->
  <rect x="24" y="18" width="{tag_len:.0f}" height="18" rx="9" fill="{tag_col}" fill-opacity="0.12" stroke="{tag_col}" stroke-opacity="0.4" stroke-width="1"/>
  <text x="{24 + tag_len/2:.0f}" y="30" text-anchor="middle" fill="{tag_col}" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="700" letter-spacing="1.5">{escape(project["tag"])}</text>

  <!-- Project name -->
  <text x="24" y="64" fill="{PALETTE["WHITE"]}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="26" font-weight="800">{escape(project["name"])}</text>

  <!-- Description -->
  <text x="24" y="85" fill="{PALETTE["MUTED"]}" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="12" font-weight="400">{escape(project["desc"][:90])}</text>

  <!-- Language strip -->
  <text x="24" y="100" fill="{lang_col}" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="600" letter-spacing="0.5">{escape(project["lang"])}</text>

  <!-- Arrow indicator -->
  <text x="{CARD_W - 24}" y="60" text-anchor="end" fill="{acc}" font-family="'JetBrains Mono', monospace" font-size="20" font-weight="700">→</text>
  <text x="{CARD_W - 24}" y="80" text-anchor="end" fill="{PALETTE["SLATE"]}" font-family="'JetBrains Mono', monospace" font-size="10">VIEW REPO</text>
</svg>'''

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    size_kb = out.stat().st_size / 1024
    print(f"[✓] Project card → {out} ({size_kb:.1f} KB)")


def main():
    for project in PROJECTS:
        path = f"assets/projects/{project['id']}.svg"
        generate_card(project, path)


if __name__ == "__main__":
    main()
