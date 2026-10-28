#!/usr/bin/env python3
"""
TACE-X Engineering Arsenal Visual Showcase Generator
=====================================================
Generates:
  assets/tech-grid.svg
  assets/tech-strip.svg (mirrored for backward compatibility)

Renders the cybernetic futuristic developer showcase inspired by the reference image:
  - Cybernetic HUD bezel frame with chamfered angular corner brackets and neon accents.
  - TACE-X personal falcon emblem centered above the main title.
  - Heading: "ENGINEERING ARSENAL" (white + cyan).
  - Subtitle: "20+ TECHNOLOGIES · ONE BUILDER · BUILT TO SHIP".
  - Top-right HUD status: "CODE // BUILD // DEPLOY // REPEAT".
  - 7 Structured Categories across 2 rows:
      1. Web Development (HTML, CSS, JavaScript, TypeScript)
      2. Backend & Systems (Python, Java, Rust, Node.js)
      3. Frontend & Frameworks (React, Tailwind CSS, Vite)
      4. Mobile & App Development (Swift, SwiftUI, Kotlin)
      5. Cloud & Services (Firebase, Supabase)
      6. Tools & Version Control (Git, Docker)
      7. Platforms & OS (macOS, Linux)
  - Bottom console bar:
      "> BUILDING IDEAS INTO REALITY..."  //  "DEV · DESIGN · AUTOMATE · DEPLOY"
  - Restrained SVG native animations (@keyframes textGlow, framePulse) with prefers-reduced-motion support.
"""

from pathlib import Path
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "assets" / "tech-grid.svg"
LEGACY_FILE = REPO_ROOT / "assets" / "tech-strip.svg"

# Extract exact falcon emblem path from assets/branding/tace-x-emblem.svg
EMBLEM_FILE = REPO_ROOT / "assets" / "branding" / "tace-x-emblem.svg"
tree = ET.parse(EMBLEM_FILE)
root = tree.getroot()
ns = {"svg": "http://www.w3.org/2000/svg"}
emblem_paths = [el.attrib.get("d") for el in root.iter() if el.tag.endswith("path") and "d" in el.attrib]

CATEGORIES = [
    # ─── ROW 1 ───
    {
        "id": "web",
        "title": "WEB DEVELOPMENT",
        "count": "4",
        "row": 1,
        "width": 272,
        "x": 20,
        "y": 96,
        "h": 160,
        "items": [
            {
                "id": "html",
                "name": "HTML",
                "accent": "#F97316",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <path d="M4 2l1.8 20 7.2 2 7.2-2L22 2H4z" fill="#F97316" fill-opacity="0.2" stroke="#F97316" stroke-width="1.2"/>
                    <path d="M13 4v18.1l5.4-1.5 1.5-16.6H13z" fill="#F97316" fill-opacity="0.35"/>
                    <path d="M7.5 6.5h11l-.3 3.6H11.3l.2 2.9h6.4l-.7 7.2-4.2 1.2-4.2-1.2-.3-3.4H11l.1 1.6 1.9.5 1.9-.5.3-3.5H8L7.5 6.5z" fill="#F8FAFC"/>
                  </g>
                """
            },
            {
                "id": "css",
                "name": "CSS",
                "accent": "#38BDF8",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <path d="M4 2l1.8 20 7.2 2 7.2-2L22 2H4z" fill="#38BDF8" fill-opacity="0.2" stroke="#38BDF8" stroke-width="1.2"/>
                    <path d="M13 4v18.1l5.4-1.5 1.5-16.6H13z" fill="#38BDF8" fill-opacity="0.35"/>
                    <path d="M7.5 6.5h11l-1 11-4.5 1.3-4.5-1.3-.3-3.4h2.4l.1 1.6 2.3.6 2.3-.6.5-4.5H9.5l-.3-3.4h8.3l.3-3.1H7.5V6.5z" fill="#F8FAFC"/>
                  </g>
                """
            },
            {
                "id": "js",
                "name": "JavaScript",
                "accent": "#F59E0B",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <rect x="2" y="2" width="24" height="24" rx="4.5" fill="#1C1408" stroke="#F59E0B" stroke-width="1.2"/>
                    <path d="M9.5 10v8.5c0 2-1.1 2.8-2.8 2.8-1.1 0-2-.5-2.5-1.1l1.4-1.6c.3.4.7.6 1.1.6.6 0 .9-.3.9-1.1V10h1.9z" fill="#F8FAFC"/>
                    <path d="M20.8 12.5c-.5-.7-1.3-1-2.3-1-1.4 0-2.3.8-2.3 1.8 0 1.1.7 1.6 2.1 2.1 1.5.5 2.7 1 2.7 2.7 0 1.8-1.5 2.8-3.3 2.8-1.4 0-2.5-.5-3.3-1.4l1.3-1.8c.6.6 1.3 1 2.1 1 .9 0 1.5-.5 1.5-1 0-.7-.6-1-1.9-1.6-1.7-.6-2.9-1.2-2.9-2.6 0-1.7 1.4-2.8 3.3-2.8 1.1 0 2.2.3 3 1l-1.2 1.8z" fill="#F59E0B"/>
                  </g>
                """
            },
            {
                "id": "ts",
                "name": "TypeScript",
                "accent": "#00E5FF",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <rect x="2" y="2" width="24" height="24" rx="4.5" fill="#071A2E" stroke="#00E5FF" stroke-width="1.2"/>
                    <path d="M6 9h8v2H11v8.5H8.5V11H6V9z" fill="#94A3B8"/>
                    <path d="M21.5 11.5c-.5-.7-1.3-1-2.3-1-1.4 0-2.3.8-2.3 1.8 0 1.1.7 1.6 2.1 2.1 1.5.5 2.7 1 2.7 2.7 0 1.8-1.5 2.8-3.3 2.8-1.4 0-2.5-.5-3.3-1.4l1.3-1.8c.6.6 1.3 1 2.1 1 .9 0 1.5-.5 1.5-1 0-.7-.6-1-1.9-1.6-1.7-.6-2.9-1.2-2.9-2.6 0-1.7 1.4-2.8 3.3-2.8 1.1 0 2.2.3 3 1l-1.2 1.8z" fill="#00E5FF"/>
                  </g>
                """
            }
        ]
    },
    {
        "id": "backend",
        "title": "BACKEND & SYSTEMS",
        "count": "4",
        "row": 1,
        "width": 272,
        "x": 302,
        "y": 96,
        "h": 160,
        "items": [
            {
                "id": "python",
                "name": "Python",
                "accent": "#38BDF8",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <path d="M13.8 2.5c-4 0-3.8 1.7-3.8 1.7l.01 1.8h3.8v.6H7c0 0-2.6.4-2.6 3.8s2.2 3.6 2.2 3.6h1.3v-1.9c0-2.2 1.9-2.2 1.9-2.2h3.8c1.9 0 1.9-1.7 1.9-1.7V4.7S15.6 2.5 13.8 2.5zm-1 1.2a.7.7 0 1 1 0 1.4.7.7 0 0 1 0-1.4z" fill="#38BDF8"/>
                    <path d="M14.2 25.5c4 0 3.8-1.7 3.8-1.7l-.01-1.8h-3.8v-.6H21c0 0 2.6-.4 2.6-3.8s-2.2-3.6-2.2-3.6h-1.3v1.9c0 2.2-1.9 2.2-1.9 2.2h-3.8c-1.9 0-1.9 1.7-1.9 1.7v2.7s-.2 2.2 1.7 2.2zm1-1.2a.7.7 0 1 1 0-1.4.7.7 0 0 1 0 1.4z" fill="#F59E0B"/>
                  </g>
                """
            },
            {
                "id": "java",
                "name": "Java",
                "accent": "#F43F5E",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <path d="M11.5 3c1 1.8-1 3 0 4.8" fill="none" stroke="#F43F5E" stroke-width="1.3" stroke-linecap="round"/>
                    <path d="M15 2.5c1 2-1 3.5 0 5.2" fill="none" stroke="#F59E0B" stroke-width="1.3" stroke-linecap="round"/>
                    <path d="M18.5 3.5c1 1.5-1 2.5 0 4.2" fill="none" stroke="#F43F5E" stroke-width="1.3" stroke-linecap="round"/>
                    <path d="M7 11.5h13v6c0 2.5-2 4.5-4.5 4.5h-4c-2.5 0-4.5-2-4.5-4.5v-6z" fill="#F43F5E" fill-opacity="0.2" stroke="#F43F5E" stroke-width="1.3"/>
                    <path d="M20 13h1.8a2.2 2.2 0 0 1 0 4.4H20" fill="none" stroke="#F43F5E" stroke-width="1.3"/>
                    <path d="M5.5 23.5h17" stroke="#94A3B8" stroke-width="1.4" stroke-linecap="round"/>
                  </g>
                """
            },
            {
                "id": "rust",
                "name": "Rust",
                "accent": "#FB923C",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <path d="M12.5 2h3l.6 2.8c.7.2 1.4.6 2.1 1l2.6-1.5 2 2-1.5 2.6c.4.7.8 1.4 1 2.1l2.8.6v3l-2.8.6c-.2.7-.6 1.4-1 2.1l1.5 2.6-2 2-2.6-1.5c-.7.4-1.4.8-2.1 1l-.6 2.8h-3l-.6-2.8c-.7-.2-1.4-.6-2.1-1l-2.6 1.5-2-2 1.5-2.6c-.4-.7-.8-1.4-1-2.1L3.4 15v-3l2.8-.6c.2-.7.6-1.4 1-2.1L5.7 6.7l2-2 2.6 1.5c.7-.4 1.4-.8 2.1-1L12.5 2z" fill="#080D15" stroke="#FB923C" stroke-width="1.3"/>
                    <circle cx="14" cy="14" r="5.5" fill="#0B1220" stroke="#00E5FF" stroke-width="1.1"/>
                    <path d="M11.5 10.5h3c1.1 0 1.8.6 1.8 1.5 0 .8-.6 1.4-1.4 1.5l1.6 3.9h-1.5l-1.4-3.6h-.7v3.6h-1.4v-6.9zm1.4 2.4h1.4c.4 0 .7-.2.7-.7s-.3-.7-.7-.7h-1.4v1.4z" fill="#F8FAFC"/>
                  </g>
                """
            },
            {
                "id": "node",
                "name": "Node.js",
                "accent": "#10B981",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <path d="M14 2.5l10 5.6v11.2L14 24.9 4 19.3V8.1L14 2.5z" fill="#071A12" stroke="#10B981" stroke-width="1.3"/>
                    <path d="M10 9v10l8-4.6V4.4L10 9zm2.1 3.1l4.2-2.4v6.3l-4.2 2.4V12.1z" fill="#F8FAFC"/>
                  </g>
                """
            }
        ]
    },
    {
        "id": "frontend",
        "title": "FRONTEND & FRAMEWORKS",
        "count": "3",
        "row": 1,
        "width": 246,
        "x": 584,
        "y": 96,
        "h": 160,
        "items": [
            {
                "id": "react",
                "name": "React",
                "accent": "#00E5FF",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <circle cx="14" cy="14" r="2.6" fill="#00E5FF"/>
                    <ellipse cx="14" cy="14" rx="11" ry="4.4" fill="none" stroke="#00E5FF" stroke-width="1.2"/>
                    <ellipse cx="14" cy="14" rx="11" ry="4.4" fill="none" stroke="#38BDF8" stroke-width="1.2" transform="rotate(60 14 14)"/>
                    <ellipse cx="14" cy="14" rx="11" ry="4.4" fill="none" stroke="#818CF8" stroke-width="1.2" transform="rotate(120 14 14)"/>
                  </g>
                """
            },
            {
                "id": "tailwind",
                "name": "Tailwind CSS",
                "accent": "#00E5FF",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <path d="M7.5 11.5c1.4-2.8 3.5-4 5.8-3.3 1.9.6 2.8 1.9 4 3 1.3 1.4 2.7 2.9 5.4 2.9 2.4 0 4-1.4 5-4-1.3 1-2.7 1.4-4.1.8-1.5-.6-2.6-1.9-3.7-3-1.3-1.4-2.7-2.9-5.4-2.9-2.6 0-4.2 1.4-5.1 4l-1.9 2.5z" fill="#00E5FF"/>
                    <path d="M2.5 18.5c1.4-2.8 3.5-4 5.8-3.3 1.9.6 2.8 1.9 4 3 1.3 1.4 2.7 2.9 5.4 2.9 2.4 0 4-1.4 5-4-1.3 1-2.7 1.4-4.1.8-1.5-.6-2.6-1.9-3.7-3-1.3-1.4-2.7-2.9-5.4-2.9-2.6 0-4.2 1.4-5.1 4L2.5 18.5z" fill="#38BDF8"/>
                  </g>
                """
            },
            {
                "id": "vite",
                "name": "Vite",
                "accent": "#8B5CF6",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <path d="M24.5 5.5L14 25.5 3.5 5.5h21z" fill="#140D2E" stroke="#8B5CF6" stroke-width="1.3"/>
                    <path d="M17.5 4L10 15h5l-2.4 8 8.2-12.2h-5.2L17.5 4z" fill="#00E5FF"/>
                  </g>
                """
            }
        ]
    },

    # ─── ROW 2 ───
    {
        "id": "mobile",
        "title": "MOBILE & APP DEVELOPMENT",
        "count": "3",
        "row": 2,
        "width": 240,
        "x": 20,
        "y": 266,
        "h": 160,
        "items": [
            {
                "id": "swift",
                "name": "Swift",
                "accent": "#F97316",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <rect x="2" y="2" width="24" height="24" rx="5" fill="#1F0F07" stroke="#F97316" stroke-width="1.2"/>
                    <path d="M22 17.5c-.7.5-3 2.1-5.7 1.3-2.9-.9-5.2-3.3-6.5-5.9 1.4 1.2 3.4 1.8 5.1 1.2-1.7-.8-3.1-2.3-3.8-4.1-.7-1.7-.7-3.4-.2-4.9.4 1.6 1.4 3 2.8 4 1.8 1.3 4 1.8 6.2 1.5-1.1-.9-1.9-2.2-2.1-3.6 2.3 2 4.4 4.5 4.9 7.4.2 1.1 0 2.2-.7 3.1z" fill="#FB923C"/>
                  </g>
                """
            },
            {
                "id": "swiftui",
                "name": "SwiftUI",
                "accent": "#00E5FF",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <rect x="2" y="2" width="24" height="24" rx="5" fill="#07192A" stroke="#00E5FF" stroke-width="1.2"/>
                    <circle cx="14" cy="14" r="7.5" fill="none" stroke="#00E5FF" stroke-width="1.2" stroke-dasharray="3 2"/>
                    <path d="M10 14c0-2.2 1.8-4 4-4s4 1.8 4 4-1.8 4-4 4" fill="none" stroke="#38BDF8" stroke-width="1.8" stroke-linecap="round"/>
                    <circle cx="14" cy="14" r="1.8" fill="#F8FAFC"/>
                  </g>
                """
            },
            {
                "id": "kotlin",
                "name": "Kotlin",
                "accent": "#7C3AED",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <rect x="2" y="2" width="24" height="24" rx="5" fill="#180C2E" stroke="#7C3AED" stroke-width="1.2"/>
                    <path d="M5 5h18L14 14l9 9H5V5z" fill="#7C3AED" fill-opacity="0.3"/>
                    <path d="M5 5l9 9-9 9V5z" fill="#00E5FF"/>
                    <path d="M14 14l9-9H5l9 9z" fill="#7C3AED"/>
                    <path d="M14 14l9 9H5l9-9z" fill="#F97316"/>
                  </g>
                """
            }
        ]
    },
    {
        "id": "cloud",
        "title": "CLOUD & SERVICES",
        "count": "2",
        "row": 2,
        "width": 180,
        "x": 270,
        "y": 266,
        "h": 160,
        "items": [
            {
                "id": "firebase",
                "name": "Firebase",
                "accent": "#F59E0B",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <path d="M5 20.5l3.2-14.5c.1-.6.8-.7 1.2-.2l3.6 5L5 20.5z" fill="#F59E0B" fill-opacity="0.8"/>
                    <path d="M5 20.5l18-3.9L16.5 3.5c-.3-.6-1.1-.6-1.3 0L5 20.5z" fill="#F59E0B"/>
                    <path d="M23 16.6l-3.2-6c-.2-.4-.8-.6-1.1-.1L5 20.5l13.2 3.2c.9.2 2-.2 2.2-1.1l2.6-6z" fill="#00E5FF"/>
                  </g>
                """
            },
            {
                "id": "supabase",
                "name": "Supabase",
                "accent": "#10B981",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <path d="M15 3.5c-.4-.7-1.5-.7-1.8 0L4.2 18.2c-.4.7.1 1.6 1 1.6H13l-1.5 5.7c-.2.7.7 1.2 1.2.6l9.6-11.7c.5-.6.1-1.6-.8-1.6H14l1-9.3z" fill="#10B981"/>
                    <path d="M13 3.5L4.2 18.2c-.4.7.1 1.6 1 1.6H13l-1.5 5.7c-.2.7.7 1.2 1.2.6L16 22V9.5l-3-6z" fill="#34D399" fill-opacity="0.8"/>
                  </g>
                """
            }
        ]
    },
    {
        "id": "tools",
        "title": "TOOLS & VERSION CONTROL",
        "count": "2",
        "row": 2,
        "width": 186,
        "x": 460,
        "y": 266,
        "h": 160,
        "items": [
            {
                "id": "git",
                "name": "Git",
                "accent": "#F43F5E",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <rect x="4" y="4" width="20" height="20" rx="3.5" fill="#1C0E0B" stroke="#F43F5E" stroke-width="1.3" transform="rotate(45 14 14)"/>
                    <circle cx="9" cy="19" r="2" fill="#00E5FF"/>
                    <circle cx="19" cy="9" r="2" fill="#F8FAFC"/>
                    <circle cx="19" cy="19" r="2" fill="#F8FAFC"/>
                    <path d="M9 19h5.5a4 4 0 0 0 4-4V9" fill="none" stroke="#00E5FF" stroke-width="1.3"/>
                    <line x1="19" y1="19" x2="19" y2="14" stroke="#F8FAFC" stroke-width="1.3"/>
                  </g>
                """
            },
            {
                "id": "docker",
                "name": "Docker",
                "accent": "#38BDF8",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <!-- Containers -->
                    <rect x="7" y="10" width="3" height="3" rx="0.5" fill="#38BDF8"/>
                    <rect x="11" y="10" width="3" height="3" rx="0.5" fill="#38BDF8"/>
                    <rect x="15" y="10" width="3" height="3" rx="0.5" fill="#38BDF8"/>
                    <rect x="11" y="6" width="3" height="3" rx="0.5" fill="#38BDF8"/>
                    <rect x="15" y="6" width="3" height="3" rx="0.5" fill="#38BDF8"/>
                    <!-- Whale body -->
                    <path d="M25 13c-.4-.1-1.6-.2-2.5.5-.3-.9-1-1.6-1.9-1.9L20 13c-.2 0-3-.1-5.5 1.5H3c-.3 1.2 0 4.2 2.5 6.2 3.1 2.5 8 2.3 11.5 2.3 5 0 8.5-3 9-8-.3-.7-.7-1.4-1-2z" fill="#0284C7"/>
                    <circle cx="6" cy="17" r="0.8" fill="#070D18"/>
                  </g>
                """
            }
        ]
    },
    {
        "id": "platforms",
        "title": "PLATFORMS & OS",
        "count": "2",
        "row": 2,
        "width": 184,
        "x": 656,
        "y": 266,
        "h": 160,
        "items": [
            {
                "id": "macos",
                "name": "macOS",
                "accent": "#F8FAFC",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <!-- Apple leaf -->
                    <path d="M17.5 4.5c-.8 1-2 1.7-3.1 1.6-.3-1.1.3-2.3 1-3 .8-.9 2.1-1.5 3.1-1.5.2 1.1-.2 2.1-1 2.9z" fill="#00E5FF"/>
                    <!-- Apple body -->
                    <path d="M22.5 17.5c-.6 1.4-1.3 2.7-2.3 3.8-1.4 1.4-2.8 1.5-4.3.8-1.4-.7-2.7-.7-4.2 0-1.5.7-2.8.6-4.1-.8-1.9-2.1-3.3-6-3.3-9.5 0-3.5 1.8-5.3 3.6-5.3 1.4 0 2.6.9 3.5.9.8 0 2.3-.9 3.9-.9 1.5 0 2.8.6 3.7 1.8-3.2 1.7-2.7 6.2.5 7.5-.7 1.9-1.5 3.9-2.4 5.3l1.4-.6z" fill="#F8FAFC"/>
                  </g>
                """
            },
            {
                "id": "linux",
                "name": "Linux",
                "accent": "#F59E0B",
                "icon": """
                  <g transform="translate(-14, -14)">
                    <!-- Tux silhouette -->
                    <path d="M14 3c-3 0-5 2.5-5 5.5v3c-1.5 1.5-2.5 4-2.5 6.5 0 2 1.5 3.5 3 4l-1.5 2h4l2-1.5 2 1.5h4l-1.5-2c1.5-.5 3-2 3-4 0-2.5-1-5-2.5-6.5v-3C19 5.5 17 3 14 3z" fill="#F8FAFC"/>
                    <path d="M14 4.5c-2 0-3.5 1.8-3.5 4v3.5c0 .3.2.5.5.5h6c.3 0 .5-.2.5-.5V8.5c0-2.2-1.5-4-3.5-4z" fill="#070D18"/>
                    <!-- Beak -->
                    <path d="M12 9.5h4l-2 2.5-2-2.5z" fill="#F59E0B"/>
                    <!-- Feet -->
                    <path d="M8 23.5c1.5 0 3-.5 3-1.5s-1.5-1-3-1-2.5.5-2.5 1.5 1 1 2.5 1zM20 23.5c1.5 0 3-.5 3-1.5s-1.5-1-3-1-2.5.5-2.5 1.5 1 1 2.5 1z" fill="#F59E0B"/>
                  </g>
                """
            }
        ]
    }
]

def generate_svg():
    width = 860
    height = 480

    # Build category panels
    categories_svg = []
    for cat in CATEGORIES:
        cx, cy, cw, ch = cat["x"], cat["y"], cat["width"], cat["h"]
        c_title = cat["title"]
        c_title_xml = c_title.replace("&", "&amp;")
        c_count = cat["count"]

        # Category box
        box = f"""
    <!-- Category: {c_title} -->
    <g id="cat-{cat['id']}">
      <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="10" fill="#080D15" stroke="#16243A" stroke-width="1.2"/>
      <!-- Subtle top-left cyan notch -->
      <path d="M{cx} {cy+14}V{cy+4}A4 4 0 0 1 {cx+4} {cy}H{cx+18}" stroke="#00E5FF" stroke-width="1.5" stroke-linecap="round" fill="none"/>
      
      <!-- Category Header Bar -->
      <text x="{cx+16}" y="{cy+24}" fill="#00E5FF" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="800" letter-spacing="1">{c_title_xml}</text>
      <text x="{cx+cw-16}" y="{cy+24}" text-anchor="end" fill="#8CA3BD" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="700" letter-spacing="0.5">// {c_count}</text>
      <line x1="{cx+12}" y1="{cy+34}" x2="{cx+cw-12}" y2="{cy+34}" stroke="#16243A" stroke-width="1"/>
      
      <!-- Technology Tiles -->"""

        # Position tiles inside category box
        items = cat["items"]
        n_items = len(items)
        inner_w = cw - 20
        tile_gap = 8
        tile_w = int((inner_w - (n_items - 1) * tile_gap) / n_items)
        tile_h = 100
        tile_y = cy + 44

        for ti, item in enumerate(items):
            tx = cx + 10 + ti * (tile_w + tile_gap)
            icon_cx = tx + tile_w // 2
            icon_cy = tile_y + 36
            label_y = tile_y + 80

            tile = f"""
        <!-- {item['name']} Tile -->
        <g id="tile-{item['id']}">
          <title>{item['name']}</title>
          <rect x="{tx}" y="{tile_y}" width="{tile_w}" height="{tile_h}" rx="8" fill="#0B1220" stroke="#1E304E" stroke-width="1"/>
          <!-- Top edge brand glow accent -->
          <line x1="{tx+8}" y1="{tile_y+1}" x2="{tx+tile_w-8}" y2="{tile_y+1}" stroke="{item['accent']}" stroke-width="1.5" stroke-linecap="round" stroke-opacity="0.8"/>
          <!-- Icon -->
          <g transform="translate({icon_cx}, {icon_cy})">
            {item['icon']}
          </g>
          <!-- Label -->
          <text x="{icon_cx}" y="{label_y}" text-anchor="middle" fill="#F1F5F9" font-family="'JetBrains Mono', -apple-system, sans-serif" font-size="9.5" font-weight="700" letter-spacing="0.3">{item['name']}</text>
        </g>"""
            box += tile

        box += "\n    </g>"
        categories_svg.append(box)

    # Build Falcon Emblem paths
    emblem_paths_joined = "\n".join(f'<path d="{p}" fill="#00E5FF" fill-opacity="0.95"/>' for p in emblem_paths)

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <title>ENGINEERING ARSENAL — TACE-X Engineering Identity &amp; Technology Stack</title>
  <desc>Categorized professional engineering arsenal spanning Web Development, Backend &amp; Systems, Frontend &amp; Frameworks, Mobile &amp; App Development, Cloud, Tools, and Platforms.</desc>

  <defs>
    <!-- Cyan Cybernetic Glow -->
    <filter id="cyanGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00E5FF"/>
      <stop offset="50%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#168BFF"/>
    </linearGradient>

    <linearGradient id="bezelBorder" x1="0" y1="0" x2="{width}" y2="{height}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.8"/>
      <stop offset="25%" stop-color="#168BFF" stop-opacity="0.4"/>
      <stop offset="75%" stop-color="#16243A"/>
      <stop offset="100%" stop-color="#00E5FF" stop-opacity="0.7"/>
    </linearGradient>
  </defs>

  <style>
    @keyframes sweepGlow {{
      0%, 100% {{ opacity: 0.7; }}
      50% {{ opacity: 1.0; filter: drop-shadow(0 0 6px rgba(0, 229, 255, 0.6)); }}
    }}
    .arsenal-title {{
      animation: sweepGlow 4s ease-in-out infinite;
    }}
    @media (prefers-reduced-motion: reduce) {{
      .arsenal-title {{ animation: none; }}
    }}
  </style>

  <!-- ─── OUTER CYBERNETIC BEZEL FRAME ─── -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" rx="14" fill="#05080D" stroke="url(#bezelBorder)" stroke-width="1.5"/>

  <!-- Chamfered Corner Notches -->
  <path d="M2 24V14L14 2H34" stroke="#00E5FF" stroke-width="2" fill="none"/>
  <path d="M{width-2} 24V14L{width-14} 2H{width-34}" stroke="#00E5FF" stroke-width="2" fill="none"/>
  <path d="M2 {height-24}V{height-14}L14 {height-2}H34" stroke="#00E5FF" stroke-width="2" fill="none"/>
  <path d="M{width-2} {height-24}V{height-14}L{width-14} {height-2}H{width-34}" stroke="#00E5FF" stroke-width="2" fill="none"/>

  <!-- Top Center Bezel Crest -->
  <path d="M{width//2 - 90} 2H{width//2 + 90}" stroke="#00E5FF" stroke-width="2.5"/>
  <path d="M{width//2 - 120} 2L{width//2 - 90} 14H{width//2 + 90}L{width//2 + 120} 2" fill="#080D15" stroke="#168BFF" stroke-width="1.2"/>

  <!-- ─── CREST FALCON EMBLEM (TACE-X) ─── -->
  <g transform="translate({width//2 - 18}, 14) scale(0.035)" filter="url(#cyanGlow)">
    {emblem_paths_joined}
  </g>

  <!-- ─── MAIN HEADER ─── -->
  <g class="arsenal-title">
    <text x="{width//2}" y="54" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', sans-serif" font-size="22" font-weight="900" letter-spacing="2">
      <tspan fill="#F1F5F9">ENGINEERING </tspan>
      <tspan fill="#00E5FF">ARSENAL</tspan>
    </text>
  </g>

  <!-- Subtitle -->
  <text x="{width//2}" y="74" text-anchor="middle" fill="#8CA3BD" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" letter-spacing="1.5">20+ TECHNOLOGIES  ·  ONE BUILDER  ·  BUILT TO SHIP</text>

  <!-- Top-Right Telemetry -->
  <g transform="translate({width - 80}, 24)">
    <text x="0" y="8" text-anchor="end" fill="#00E5FF" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" letter-spacing="1">CODE —</text>
    <text x="0" y="19" text-anchor="end" fill="#8CA3BD" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" letter-spacing="1">BUILD</text>
    <text x="0" y="30" text-anchor="end" fill="#8CA3BD" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" letter-spacing="1">DEPLOY</text>
    <text x="0" y="41" text-anchor="end" fill="#00E5FF" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" letter-spacing="1">REPEAT</text>
  </g>

  <!-- Header Separator Line -->
  <line x1="24" y1="86" x2="{width-24}" y2="86" stroke="#16243A" stroke-width="1.2"/>
  <circle cx="{width//2}" cy="86" r="3" fill="#00E5FF"/>

  <!-- ─── 7 CATEGORY PANELS (ROW 1 & ROW 2) ─── -->
  {''.join(categories_svg)}

  <!-- ─── BOTTOM CONSOLE BAR ─── -->
  <line x1="24" y1="442" x2="{width-24}" y2="442" stroke="#16243A" stroke-width="1.2"/>
  <text x="28" y="462" fill="#00E5FF" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700" letter-spacing="1">&gt; BUILDING IDEAS INTO REALITY...</text>
  <text x="{width-28}" y="462" text-anchor="end" fill="#8CA3BD" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="700" letter-spacing="1.2">DEV  ·  DESIGN  ·  AUTOMATE  ·  DEPLOY</text>
</svg>
"""

    OUTPUT_FILE.write_text(svg_content, encoding="utf-8")
    LEGACY_FILE.write_text(svg_content, encoding="utf-8")
    print(f"[✓] Generated Engineering Arsenal -> {OUTPUT_FILE} and {LEGACY_FILE} (20 technologies across 7 categories)")

if __name__ == "__main__":
    generate_svg()
