# TACE-X Contribution Space Shooter & Arcade Playfield
## Engineering Specification, Gamification Mechanics & Reproduction Guide

This document specifies the Phase 3 arcade space shooter engine—translating GitHub's 52-week contribution activity into an authentic, animated retro-futuristic arcade environment.

---

## 1. Gamification Mechanics & Contribution Mapping

The $53 \times 7$ contribution matrix (371 cells spanning 52 weeks + remaining days) is mapped directly into an alien armada:

| Contribution Level | Real Activity | Alien Ship Class | Behavior / Armor | Base Points | Palette Token |
|---|---|---|---|:---:|---|
| **Level 0** | 0 contributions | Space Debris / Dormant Cell | Static obstacle | +0 pts (or +5) | `#111C2D` (Shadow) |
| **Level 1** | 1–3 contributions | Scout Drone | Light hull, high-frequency hover | +10 pts | `#10B981` (Arcade Mint) |
| **Level 2** | 4–6 contributions | Armored Escort | Dual energy vanes, 2 hits to breach | +25 pts | `#00F0FF` (Electric Cyan) |
| **Level 3** | 7–9 contributions | Heavy Battlecruiser | Armored hull, 3 hits to breach | +50 pts | `#8B5CF6` (Deep Violet) |
| **Level 4** | 10+ contributions | Boss Mothership | Shielded perimeter, 5 hits to breach | +100 pts | `#F43F5E` (Cyber Threat Red) |

---

## 2. Mathematically Verified Score Formula

To ensure complete data integrity, the score displayed in the HUD is not an arbitrary fiction; it is derived from real contribution counts and intensity tiers:

$$\text{Base Score} = \sum_{i=1}^{N_{\text{days}}} \left( L_1 \times 10 + L_2 \times 25 + L_3 \times 50 + L_4 \times 100 \right)$$

$$\text{Clearance Bonus} = \text{Total Contributions} \times 5$$

$$\text{Final HUD Score} = \text{Base Score} + \text{Clearance Bonus}$$

### Verified Profile Calculation (`tace-x`):
- Total Contributions: `480`
- Level 0: 277 days
- Level 1: 72 days $\times 10 = 720\text{ PTS}$
- Level 2: 12 days $\times 25 = 300\text{ PTS}$
- Level 3: 5 days $\times 50 = 250\text{ PTS}$
- Level 4: 4 days $\times 100 = 400\text{ PTS}$
- Base Score: $720 + 300 + 250 + 400 = 1,670\text{ PTS}$
- Clearance Bonus: $480 \times 5 = 2,400\text{ PTS}$
- Baseline HUD Score: $\mathbf{4,070\text{ PTS}}$
- In-Animation Active Score: Starts at `03870`, ticks to `03970` on first target hit, and settles at $\mathbf{04070\text{ PTS}}$ upon fleet clearance!

---

## 3. Generated Assets Specification

| Asset Path | Format | Dimensions | Size | Purpose |
|---|---|---|---|---|
| [`assets/arcade/arcade_shooter.gif`](file:///Users/immanuelmelbin/tace-x/assets/arcade/arcade_shooter.gif) | GIF89a | 840 × 340 | ~141 KB | 48-frame looping arcade space shooter animation for README display. |
| [`assets/arcade/arcade_poster.svg`](file:///Users/immanuelmelbin/tace-x/assets/arcade/arcade_poster.svg) | SVG / XML | 840 × 340 | ~24 KB | Accessible static vector poster for users with `prefers-reduced-motion: reduce`. |
| [`standalone/index.html`](file:///Users/immanuelmelbin/tace-x/standalone/index.html) | HTML5 | Responsive | ~4.2 KB | Standalone interactive retro arcade game container with CRT styling. |
| [`standalone/game.js`](file:///Users/immanuelmelbin/tace-x/standalone/game.js) | JavaScript | Canvas 2D | ~12.5 KB | 60 FPS zero-dependency game engine with synthesized Web Audio sound effects. |

---

## 4. Animation Sequence (48 Frames @ 12 FPS = 3.84s Loop)

1. **Frames 0–12 (Target Acquisition & Patrol):**
   - Player starfighter patrols rightwards along the bottom corridor ($y = 282$).
   - Contribution armada drifts with subtle sinusoidal hover oscillation.
   - HUD reports `ARMADA ENGAGED` with live score.
2. **Frames 13–19 (Cannon Salvo 1):**
   - Starfighter locks underneath column 32 and fires twin cyan plasma bolts with visible muzzle flashes.
   - Bolts streak upward with glowing energy wakes.
3. **Frames 20–26 (Critical Impact 1):**
   - Plasma bolts detonate a Level 4 Boss Mothership.
   - 8-directional radial particle burst with red, amber, and white sparks.
   - HUD updates score with `CRITICAL HIT! +100`.
4. **Frames 27–33 (Lateral Bank & Salvo 2):**
   - Starfighter banks sharply left toward column 20 and fires secondary salvo.
5. **Frames 34–40 (Impact 2 & Wave Cleared):**
   - Secondary salvo destroys Level 2 Escort with cyan/mint explosion.
   - HUD flashes `COMBO x5 // CLEARED`.
6. **Frames 41–47 (Return & Loop Settle):**
   - Starfighter glides back smoothly to center $x = 360$.
   - Explosion particles dissipate.
   - Frame 47 matches Frame 0 position and velocity for a seamless, glitch-free loop!

---

## 5. How to Run the Interactive Browser Game

The standalone game requires **zero external dependencies** or npm installs:

1. Open directly in any modern browser:
   ```bash
   open standalone/index.html
   ```
2. Or serve via any local static web server:
   ```bash
   npx serve standalone
   # or
   python3 -m http.server 8080 --directory standalone
   ```
3. Controls:
   - `◀` / `▶` or `A` / `D`: Move starfighter
   - `SPACE` / `W` / `▲`: Fire twin lasers
   - `P`: Pause / Resume
   - `R`: Restart game
   - `M`: Toggle Sound (Web Audio synthesizer)

---

## 6. How to Regenerate Arcade Assets

To refresh the arcade shooter GIF and SVG from active repository contribution data:

```bash
python3 scripts/generate_arcade.py
```

To run the automated verification test suite:

```bash
python3 scripts/generate_arcade.py --test
```
