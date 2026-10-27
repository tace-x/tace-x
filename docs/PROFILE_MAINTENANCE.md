# TACE-X // PROFILE MAINTENANCE & REGENERATION GUIDE
## Operational Runbook, Automation Workflows & Asset Engineering

This runbook provides complete, reproducible instructions for maintaining, testing, and updating the [`tace-x`](https://github.com/tace-x/tace-x) GitHub profile.

---

## 1. Quick Asset Regeneration Commands

All assets can be generated and verified locally on macOS or Linux with Python 3 and Pillow.

### A. Dot-Matrix Portrait & Particle Animation
```bash
# 1. Regenerate with default synthetic geometric architect emblem:
python3 scripts/generate_portrait.py --test

# 2. Regenerate with a custom personal headshot / avatar photo:
python3 scripts/generate_portrait.py --input /path/to/your_photo.jpg --test
```
- **Outputs:**
  - `assets/portrait/portrait_dotmatrix.svg` (Static vector dot-matrix portrait with cyber HUD)
  - `assets/portrait/portrait_assembly.gif` (Holographic particle-assembly animation)
  - `assets/portrait/portrait_static.png` (512x512 high-definition static raster preview)

### B. Contribution Arcade Space Shooter
```bash
# Regenerate arcade GIF loop & static vector poster from contribution data:
python3 scripts/generate_arcade.py --test
```
- **Outputs:**
  - `assets/arcade/arcade_shooter.gif` (48-frame looping animated space shooter, 142 KB)
  - `assets/arcade/arcade_poster.svg` (Accessible static vector poster for reduced-motion)

### C. Run Full Portfolio & Asset Integrity Validation
```bash
python3 scripts/validate_portfolio.py
```
- **Checks Performed:**
  - XML validity for all 16 SVG assets in `assets/`.
  - Frame count, dimensions, and file budget (<2.5 MB) for animated GIFs.
  - 100% of internal navigation anchor links in `README.md`.
  - 100% of local asset filepaths in `README.md`.
  - 5-factor rubric scoring calculations for all shortlisted projects.
  - ViewBox dimensions on all 900px wide project banners.

---

## 2. Dependencies & Environment

Dependencies are intentionally minimal to guarantee frictionless execution in GitHub Actions runners and local development:

```bash
# Python dependencies (Standard Library + Pillow)
pip install Pillow

# Node.js (Optional, only needed if testing standalone/game.js syntax)
node -c standalone/game.js
```

No external headless browsers (Puppeteer, Playwright), no heavy C binaries (Cairo, ImageMagick), and no proprietary compilers are required.

---

## 3. Telemetry & Data Sources

| Telemetry Element | Source | Frequency | Failure Fallback |
|---|---|---|---|
| **Arcade Space Armada** | Deterministic 53-week contribution telemetry | Daily at 00:00 UTC | Deterministic snapshot of 371 contribution cells (480 total commits, 4,070 HUD score). Never crashes. |
| **GitHub Stats Card** | Dynamic query to `github-readme-stats.vercel.app` | On-demand / Cached CDN | Rendered via Obsidian theme `#0B0F17`. |
| **Top Languages Card** | Dynamic query to `github-readme-stats.vercel.app` | On-demand / Cached CDN | Reflects verified public repository language distribution. |
| **Streak Stats Card** | Dynamic query to `github-readme-streak-stats.herokuapp.com` | On-demand / Cached CDN | Rendered with custom cyan ring `#00F0FF` and arcade mint fire `#10B981`. |

---

## 4. GitHub Actions Automation

The profile is automated by `.github/workflows/arcade-telemetry.yml`:
- **Schedule:** Runs automatically every day at 00:00 UTC (`cron: "0 0 * * *"`).
- **Manual Trigger:** Can be dispatched manually via GitHub web UI (`workflow_dispatch:`).
- **Execution Pipeline:**
  1. Checks out repository (`actions/checkout@v4`).
  2. Sets up Python 3.11 with pip cache (`actions/setup-python@v5`).
  3. Installs `Pillow`.
  4. Runs `python3 scripts/generate_arcade.py` to regenerate the arcade GIF, static poster, and contact sheet.
  5. Runs `python3 scripts/validate_portfolio.py` to assert asset integrity.
  6. Commits updated assets if changes exist: `chore(cron): refresh GitHub arcade shooter telemetry assets`.

### Required GitHub Permissions:
Under repository **Settings** ➔ **Actions** ➔ **General** ➔ **Workflow permissions**:
- Select **"Read and write permissions"**.
- Check **"Allow GitHub Actions to create and approve pull requests"**.

No personal access tokens (PATs) or custom repository secrets are required.

---

## 5. How to Update Projects & Banners

### Adding or Modifying a Featured Project:
1. Edit Section 03 in `README.md`.
2. Follow the established structure:
   - Project name & domain subtitle.
   - 900px wide vector banner (`assets/<project-name>.svg`).
   - Problem statement & core value.
   - Quickstart shell command block.
   - 4-5 bulleted architectural highlights.
   - Implementation verification notes (test count, test runner).
   - Shields.io badge tags.
3. If creating a new banner, use the template in `assets/capcam.svg` or `assets/nocap.svg` (900x360 viewBox, dark background `#0B0F17`, glowing pipeline rail, and `@media (prefers-reduced-motion: reduce)` style).
4. Run `python3 scripts/validate_portfolio.py` to verify XML and link integrity.

---

## 6. Standalone Browser Arcade Game

- Located in `standalone/index.html` and `standalone/game.js`.
- **Features:** 60 FPS HTML5 Canvas arcade space shooter, procedural Web Audio API synthesizers, touch/mobile controls, keyboard bindings (`A`/`D`, `◀`/`▶`, `Space`, `P`, `R`, `M`).
- **To Deploy via GitHub Pages:**
  1. In repository **Settings** ➔ **Pages**.
  2. Under **Build and deployment**, set Source to **Deploy from a branch**.
  3. Select branch **main**, folder **/ (root)** or configure GitHub Pages action.
  4. URL will be `https://tace-x.github.io/tace-x/standalone/`.
