# TACE-X Dot-Matrix Portrait & Particle-Assembly Pipeline
## Engineering Specification, Regeneration Workflow & Asset Architecture

This document specifies the Phase 2 image-processing pipeline that transforms any input portrait photo into a custom dot-matrix pixel-art avatar and holographic particle-assembly animation.

---

## 1. Architecture Overview

```
                                 ┌─────────────────────────┐
                                 │   Input Portrait File   │
                                 │  (PNG, JPG, JPEG, WEBP) │
                                 └────────────┬────────────┘
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    │ (If file provided & valid)                        │ (If missing / fallback)
                    ▼                                                   ▼
       ┌────────────────────────┐                          ┌────────────────────────┐
       │   Square Center-Crop   │                          │  Synthetic Cybernetic  │
       │   & Contrast Boost     │                          │    Architect Emblem    │
       └────────────┬───────────┘                          └────────────┬───────────┘
                    │                                                   │
                    ▼                                                   ▼
       ┌────────────────────────┐                          ┌────────────────────────┐
       │  LANCZOS Resampling    │                          │  64x64 Grid Geometric  │
       │     to 64x64 Grid      │                          │     Visual Matrix      │
       └────────────┬───────────┘                          └────────────┬───────────┘
                    │                                                   │
                    └─────────────────────────┬─────────────────────────┘
                                              │
                                              ▼
                                ┌───────────────────────────┐
                                │   Palette Quantization    │
                                │ (Curated 8-Color Cyber)   │
                                └─────────────┬─────────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    ▼                         ▼                         ▼
       ┌────────────────────────┐┌─────────────────────────┐┌────────────────────────┐
       │   Static Vector SVG    ││ Particle Assembly GIF   ││   Static PNG Preview   │
       │ portrait_dotmatrix.svg ││  portrait_assembly.gif  ││  portrait_static.png   │
       │      (~38 KB)          ││   (29 frames, ~169 KB)  ││       (~5.5 KB)        │
       └────────────────────────┘└─────────────────────────┘└────────────────────────┘
```

---

## 2. Design System & Palette Quantization

All pixels are quantized to the official TACE-X Cyber/Neon palette:

| Token | Hex | RGB | Semantic Role |
|---|---|---|---|
| **VOID** | `#0B0F17` | `(11, 15, 23)` | Background canvas & negative space |
| **DARK_CYANITE** | `#070A0F` | `(7, 10, 15)` | Backplane grid lines & deep shadow |
| **SHADOW** | `#111C2D` | `(17, 28, 45)` | Silhouette contour & ambient dots |
| **MID_SHADOW** | `#1E293B` | `(30, 41, 59)` | Midtone depth & HUD framing |
| **CYAN** | `#00F0FF` | `(0, 240, 255)` | Ocular visor, optics & primary accent |
| **MINT** | `#10B981` | `(16, 185, 129)` | Telemetry traces & live indicators |
| **VIOLET** | `#8B5CF6` | `(139, 92, 246)` | Cranium neural lattice & AI nodes |
| **RED** | `#F43F5E` | `(244, 63, 94)` | Tactical comms beacon & threat highlights |
| **WHITE** | `#F8FAFC` | `(248, 250, 252)` | Specular glares & brightest highlights |

---

## 3. Generated Assets Specification

| Asset Path | Format | Dimensions | Size | Purpose |
|---|---|---|---|---|
| [`assets/portrait/portrait_dotmatrix.svg`](file:///Users/immanuelmelbin/tace-x/assets/portrait/portrait_dotmatrix.svg) | SVG (XML) | 512 × 512 | ~38 KB | Scalable vector dot matrix for static display & reduced-motion fallback |
| [`assets/portrait/portrait_assembly.gif`](file:///Users/immanuelmelbin/tace-x/assets/portrait/portrait_assembly.gif) | GIF89a | 512 × 512 | ~169 KB | 29-frame holographic particle convergence & scanline sweep animation |
| [`assets/portrait/portrait_static.png`](file:///Users/immanuelmelbin/tace-x/assets/portrait/portrait_static.png) | PNG (Raster) | 512 × 512 | ~5.5 KB | High-resolution raster preview of the settled frame |

---

## 4. Animation Choreography

The animated GIF loop runs at 15 FPS with a duration of 2.21 seconds across 3 distinct phases:

1. **Phase 1: Particle Assembly (Frames 0–18, ~1.2s)**
   - All 64×64 active dots begin displaced into an outer vortex orbit ($r = 220–400\text{px}$).
   - Dots converge into their exact coordinate targets using cubic ease-out:
     $$e(t) = 1 - (1 - t)^3$$
   - Staggered arrival delays ensure organic particle streaming without artificial rigidity.

2. **Phase 2: Holographic Scanline Sweep (Frames 19–27, ~0.6s)**
   - A glowing electric cyan scanline sweeps horizontally across the assembled face.
   - Intersecting dots experience a transient luminance shimmer and radius expansion before settling.

3. **Phase 3: Settled Hold & Ambient Status Breathing (Frames 28–35, ~0.5s)**
   - The completed portrait rests in sharp resolution.
   - The top HUD telemetry beacon breathes softly (`#10B981`), creating a living terminal feel.
   - Loops seamlessly back to frame 0.

---

## 5. How to Regenerate Assets with Your Photo

When you are ready to use your real portrait photograph:

1. Place your headshot or photo in `assets/portrait/source.jpg` (or any path).
2. Run the generator script:
   ```bash
   python3 scripts/generate_portrait.py --input assets/portrait/source.jpg
   ```
3. To test the integrity of the regenerated assets:
   ```bash
   python3 scripts/generate_portrait.py --test
   ```
4. The script will automatically crop, enhance, quantize, and rewrite:
   - `assets/portrait/portrait_dotmatrix.svg`
   - `assets/portrait/portrait_assembly.gif`
   - `assets/portrait/portrait_static.png`

Zero additional configuration or external dependencies are required beyond Python 3 and Pillow.
