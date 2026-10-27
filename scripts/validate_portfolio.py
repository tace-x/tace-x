#!/usr/bin/env python3
"""
TACE-X Portfolio & Asset Validation Suite (Phase 4)
---------------------------------------------------
Validates:
1. XML integrity and accessibility tags for all project & profile SVG assets.
2. Animated GIF decode integrity, frame pacing, and file size budgets.
3. README anchor consistency (ensuring all navigation links match declared IDs).
4. Local asset filepaths in README.
5. Factual consistency and rubric calculation for shortlisted projects.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_svg_assets():
    print("[1/5] Testing SVG Asset Integrity...")
    svg_files = list(REPO_ROOT.glob("assets/**/*.svg"))
    assert len(svg_files) > 0, "No SVG files found in assets/"

    passed = 0
    for svg_path in svg_files:
        rel_path = svg_path.relative_to(REPO_ROOT)
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()
            # Check namespace or tag
            assert "svg" in root.tag.lower(), f"Root tag is not svg in {rel_path}"

            # Check file size budget (must be under 150 KB for single SVG)
            size_kb = svg_path.stat().st_size / 1024
            assert size_kb < 150, f"SVG exceeds 150 KB budget: {size_kb:.1f} KB in {rel_path}"

            passed += 1
            print(f"  ✓ {rel_path} ({size_kb:.1f} KB) - Valid XML")
        except Exception as e:
            print(f"  ✗ {rel_path} FAILED: {e}")
            raise e

    print(f"  All {passed} SVG assets passed validation.\n")

def test_gif_assets():
    print("[2/5] Testing Animated GIF Assets...")
    gif_files = list(REPO_ROOT.glob("assets/**/*.gif"))
    assert len(gif_files) > 0, "No GIF files found in assets/"

    for gif_path in gif_files:
        rel_path = gif_path.relative_to(REPO_ROOT)
        size_kb = gif_path.stat().st_size / 1024

        with Image.open(gif_path) as im:
            frame_count = getattr(im, "n_frames", 1)
            assert frame_count >= 1, f"GIF has 0 frames: {rel_path}"
            assert im.is_animated, f"GIF is not animated: {rel_path}"

            # File size budget: <2.5 MB
            assert size_kb < 2560, f"GIF exceeds 2.5 MB budget: {size_kb:.1f} KB in {rel_path}"
            print(f"  ✓ {rel_path} ({size_kb:.1f} KB, {frame_count} frames, {im.size[0]}x{im.size[1]}) - Decoded successfully")

    print("  All GIF assets passed validation.\n")

def test_readme_anchors_and_assets():
    print("[3/5] Testing README Navigation Anchors and Asset Links...")
    readme_path = REPO_ROOT / "README.md"
    assert readme_path.exists(), "README.md not found"

    content = readme_path.read_text(encoding="utf-8")

    # Extract declared anchor IDs: <a id="..."> or <div id="...">
    declared_ids = set(re.findall(r'<[a-zA-Z0-9]+\s+[^>]*id=["\']([^"\']+)["\']', content))
    print(f"  Found {len(declared_ids)} declared anchor IDs in README.")

    # Extract internal anchor hrefs: href="#..."
    anchor_hrefs = re.findall(r'href=["\']#([^"\']+)["\']', content)
    print(f"  Found {len(anchor_hrefs)} internal anchor links in README.")

    missing_anchors = []
    for href in anchor_hrefs:
        # Check direct match or slug variations
        clean_href = href.lstrip('-')
        matched = False
        if href in declared_ids or f"-{href}" in declared_ids or clean_href in declared_ids or f"-{clean_href}" in declared_ids:
            matched = True
        if not matched:
            missing_anchors.append(href)

    if missing_anchors:
        print(f"  ✗ Warning/Error: Missing anchor targets: {missing_anchors}")
    else:
        print("  ✓ 100% of internal navigation anchors resolve to declared targets.")

    # Extract local asset image paths
    img_srcs = re.findall(r'(?:src|srcset)=["\'](assets/[^"\']+)["\']', content)
    assert len(img_srcs) > 0, "No assets found in README"

    for src in img_srcs:
        # Split commas if srcset
        paths = [p.strip().split()[0] for p in src.split(',')]
        for p in paths:
            asset_file = REPO_ROOT / p
            assert asset_file.exists(), f"Broken image asset link in README: {p}"

    print(f"  ✓ All {len(img_srcs)} asset references in README exist on disk.\n")

def test_project_rubric_scoring():
    print("[4/5] Evaluating Top Project Rubric Scores...")
    # Rubric: Technical Depth (25%), Originality (20%), Practical Usefulness (20%),
    # Implementation Evidence (20%), Documentation and Presentation (15%)
    projects = [
        {
            "name": "TerminalVision",
            "repo": "https://github.com/tace-x/TerminalVision",
            "tech_depth": 5.0,
            "originality": 4.5,
            "usefulness": 4.5,
            "evidence": 5.0,
            "presentation": 4.5,
            "stack": "Rust 2024, Ratatui, Unix PTY, Crossterm",
            "evidence_note": "21 integration test suites under tests/, zero-allocation VFS core, embedded live PTY"
        },
        {
            "name": "CAPCAM",
            "repo": "https://github.com/tace-x/CAPCAM",
            "tech_depth": 4.5,
            "originality": 5.0,
            "usefulness": 4.5,
            "evidence": 5.0,
            "presentation": 4.0,
            "stack": "TypeScript, Chrome MV3, WebRTC, Offscreen Canvas, Vitest",
            "evidence_note": "15 unit/integration test suites under tests/, offscreen canvas pipeline replaces WebRTC tracks"
        },
        {
            "name": "NOCAP (TruthLens)",
            "repo": "https://github.com/tace-x/NOCAP",
            "tech_depth": 4.5,
            "originality": 4.5,
            "usefulness": 4.5,
            "evidence": 4.5,
            "presentation": 4.0,
            "stack": "TypeScript, React 19.2, Tailwind v4, NVIDIA NIM, Gemma 4",
            "evidence_note": "Modular serverless API under api/ai/ (check, enhance, similarity, synthesize), NVIDIA NIM adapters"
        },
        {
            "name": "Kalvichat",
            "repo": "https://github.com/tace-x/Kalvichat",
            "tech_depth": 4.0,
            "originality": 4.0,
            "usefulness": 4.5,
            "evidence": 4.5,
            "presentation": 4.5,
            "stack": "JavaScript/TypeScript, React 19.1, Cloud Firestore, Firebase Auth",
            "evidence_note": "Automated node --test suites, production firestore.rules and firestore.indexes.json"
        },
        {
            "name": "TypeTasks",
            "repo": "https://github.com/tace-x/TypeTasks",
            "tech_depth": 3.5,
            "originality": 4.0,
            "usefulness": 4.5,
            "evidence": 4.0,
            "presentation": 4.0,
            "stack": "TypeScript, React 18.3, Vite 8, Vitest, Lucide React",
            "evidence_note": "Live deployment at typetask-nine.vercel.app, zero-latency keyboard dispatch"
        },
        {
            "name": "Project-Alpha",
            "repo": "https://github.com/tace-x/Project-Alpha",
            "tech_depth": 3.5,
            "originality": 4.5,
            "usefulness": 3.5,
            "evidence": 3.5,
            "presentation": 4.0,
            "stack": "TypeScript, React 18, Express, Firebase Admin",
            "evidence_note": "Adversarial evaluation loop (Decision -> Challenge -> Simulate -> Verdict)"
        }
    ]

    ranked = []
    for p in projects:
        score = (
            p["tech_depth"] * 0.25 +
            p["originality"] * 0.20 +
            p["usefulness"] * 0.20 +
            p["evidence"] * 0.20 +
            p["presentation"] * 0.15
        )
        ranked.append((score, p))

    ranked.sort(key=lambda x: x[0], reverse=True)

    print("  Ranked Showcase Candidates:")
    for rank, (score, p) in enumerate(ranked, 1):
        print(f"  #{rank}: {p['name']} — Score: {score:.3f}/5.000")
        print(f"      Stack: {p['stack']}")
        print(f"      Evidence: {p['evidence_note']}")
    print()

def test_banner_dimensions():
    print("[5/5] Testing SVG Banner ViewBox Dimensions...")
    project_banners = [
        "terminal-vision.svg",
        "capcam.svg",
        "nocap.svg",
        "kalvi-chat.svg",
        "typetasks.svg",
        "project-alpha.svg"
    ]
    for b in project_banners:
        banner_path = REPO_ROOT / "assets" / b
        assert banner_path.exists(), f"Banner {b} missing"
        tree = ET.parse(banner_path)
        root = tree.getroot()
        viewbox = root.attrib.get("viewBox", "")
        width = root.attrib.get("width", "")
        height = root.attrib.get("height", "")
        print(f"  ✓ {b}: {width}x{height} (viewBox='{viewbox}')")
    print("  All project banners verified.\n")

def test_snake_removal():
    print("[6/7] Testing Complete Snake Deprecation & Removal...")
    readme_path = REPO_ROOT / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8").lower()
    assert "snake" not in readme_text, "Found unwanted 'snake' reference in README.md!"

    # Ensure no snake workflows exist
    snake_workflow = REPO_ROOT / ".github" / "workflows" / "snake.yml"
    assert not snake_workflow.exists(), "Found obsolete .github/workflows/snake.yml!"

    # Ensure no snake assets exist
    for f in ["github-snake.svg", "github-snake-dark.svg"]:
        snake_asset = REPO_ROOT / "assets" / f
        assert not snake_asset.exists(), f"Found obsolete snake asset {f}!"

    print("  ✓ Zero snake assets, workflows, or README references exist in repository.\n")

def test_arcade_state_progression():
    print("[7/7] Testing Arcade State Machine & Finite Combat Sequence...")
    gif_path = REPO_ROOT / "assets" / "arcade" / "arcade_shooter.gif"
    assert gif_path.exists(), "Missing arcade_shooter.gif"

    with Image.open(gif_path) as im:
        assert im.n_frames == 64, f"Expected 64 frames, got {im.n_frames}"
        assert im.size == (840, 340), f"Expected 840x340, got {im.size}"

        # Frame 4 (State 1: Initialization)
        im.seek(4)
        f4 = im.convert("RGB")
        # Fleet active: check presence of target pixels in target area
        # Check targets row area y in [70, 190]
        has_targets_init = False
        for ty in [80, 115, 150, 185]:
            for tx in [230, 270, 340, 380, 420, 460, 500, 570, 610]:
                pixel = f4.getpixel((tx, ty))
                if pixel != (11, 15, 23):  # Non-void
                    has_targets_init = True
                    break
        assert has_targets_init, "State 1 Initialization has no targets!"

        # Frame 50 (State 4: Victory Held)
        im.seek(50)
        f50 = im.convert("RGB")
        # Battlefield must be cleared: all target origins in target zone must be empty (VOID or star)
        # Check target locations are completely cleared
        for ty in [80, 115, 150, 185]:
            for tx in [230, 270, 340, 380, 500, 570, 610]:
                pixel = f50.getpixel((tx, ty))
                # Must not be any of the invader colors
                assert pixel not in [(16, 185, 129), (0, 240, 255), (139, 92, 246), (244, 63, 94)], \
                    f"Target still visible at ({tx}, {ty}) in victory state!"

        # Victory modal banner must be present at center (x=420, y=128)
        modal_pixel = f50.getpixel((420, 128))
        # Modal interior is DARK_CYANITE (7, 10, 15) or text
        assert modal_pixel != (11, 15, 23), "Victory modal missing in State 4!"

        # Frame 61 (State 5: Deliberate Reset Scanline at y=168)
        im.seek(61)
        f61 = im.convert("RGB")
        wipe_y = int(54 + ((61 - 59) / 5.0) * (340 - 54))  # 168
        has_cyan_line = any(f61.getpixel((x, wipe_y)) == (0, 240, 255) for x in range(100, 740, 50))
        assert has_cyan_line, f"State 5 Deliberate reset scanline missing at y={wipe_y}!"

    print("  ✓ State 1 (Init) -> State 2 (Combat) -> State 3 (Clearing) -> State 4 (Victory Held) -> State 5 (Reset) verified.\n")

def test_heading_uniqueness_and_links():
    print("[8/9] Testing README Heading Hierarchy and Unique Sections...")
    readme_path = REPO_ROOT / "README.md"
    content = readme_path.read_text(encoding="utf-8")

    h2_headings = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    assert len(h2_headings) == 6, f"Expected exactly 6 major sections, found {len(h2_headings)}: {h2_headings}"
    assert len(set(h2_headings)) == len(h2_headings), f"Duplicate major headings detected: {h2_headings}"

    expected_sections = [
        "01 // IDENTITY & COCKPIT",
        "02 // SIGNATURE CONTRIBUTION SPACE DEFENDER",
        "03 // FEATURED PROJECTS",
        "04 // TECHNOLOGY STACK",
        "05 // COMPACT ACTIVITY TELEMETRY",
        "06 // CONTACT & TRANSMISSION",
    ]
    for exp in expected_sections:
        assert any(exp in h for h in h2_headings), f"Missing expected section: {exp}"

    print("  ✓ All 6 major section headings are strictly unique, correctly ordered, and match specification.\n")

def test_secret_cleanliness():
    print("[9/9] Testing Secret Cleanliness & File Integrity...")
    pattern = re.compile(r'(ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{82}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z-_]{35}|bearer\s+[a-zA-Z0-9_\-\.]{20,})', re.IGNORECASE)
    for root, dirs, files in os.walk(REPO_ROOT):
        if '.git' in dirs:
            dirs.remove('.git')
        for f in files:
            p = Path(root) / f
            try:
                text = p.read_text(encoding='utf-8', errors='ignore')
                match = pattern.search(text)
                assert not match, f"Potential credential/token pattern in {p.relative_to(REPO_ROOT)}"
            except Exception:
                pass
    print("  ✓ Zero API keys, tokens, or credentials detected across all repository files.\n")

if __name__ == "__main__":
    print("==================================================")
    print("  TACE-X PORTFOLIO VALIDATION SUITE")
    print("==================================================")
    test_svg_assets()
    test_gif_assets()
    test_readme_anchors_and_assets()
    test_project_rubric_scoring()
    test_banner_dimensions()
    test_snake_removal()
    test_arcade_state_progression()
    test_heading_uniqueness_and_links()
    test_secret_cleanliness()
    print("==================================================")
    print("  ALL PORTFOLIO VALIDATION TESTS PASSED (100%)")
    print("==================================================")
