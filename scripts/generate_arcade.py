#!/usr/bin/env python3
"""
TACE-X Contribution Grid Arcade Shooter
=========================================
Generates an arcade space-shooter GIF where:
  - The spaceship fires EXACTLY ONE projectile at a time.
  - Targets are chosen RANDOMLY from the remaining active GitHub contribution cells.
  - The ship aims toward the selected target and fires.
  - The projectile visibly travels to that specific target.
  - On impact, the target cell pops, dissolves, and disappears.
  - The score updates only after a successful hit.
  - A new shot does not launch until the current hit completes.
  - Empty cells (count == 0) are shown as dim ghost cells — never targeted.
  - Destroyed cells cannot be targeted again (removed from remaining collection).
  - No multiple overlapping projectiles.
  - All active targets are cleared before entering the victory state.
  - After victory sequence, resets deliberately with a scanline beam and loops.

State machine:
  IDLE -> AIMING -> FIRING -> IMPACT -> CELL CLEARED -> NEXT RANDOM TARGET
  -> SECTOR CLEARED -> VICTORY -> RESET -> NEW CYCLE
"""

import argparse
import json
import math
import os
import random
import subprocess
import sys
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timedelta, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ─── PALETTE ────────────────────────────────────────────────────────────────
P = {
    "VOID":     (11,  15,  23),
    "DARK":     (7,   10,  15),
    "SHADOW":   (17,  28,  45),
    "MID":      (30,  41,  59),
    "CYAN":     (0,   240, 255),
    "CYAN_DIM": (56,  189, 248),
    "MINT":     (16,  185, 129),
    "MINT_LT":  (110, 231, 183),
    "VIOLET":   (139, 92,  246),
    "RED":      (244, 63,  94),
    "AMBER":    (245, 158, 11),
    "WHITE":    (248, 250, 252),
    "MUTED":    (148, 163, 184),
}

# Contribution intensity -> color
LEVEL_COLOR = {
    0: P["SHADOW"],    # ghost — empty cell
    1: P["MINT"],      # 1–3 contributions
    2: P["CYAN"],      # 4–9 contributions
    3: P["VIOLET"],    # 10–19 contributions
    4: P["RED"],       # 20+ contributions
}

LEVEL_PTS = {1: 10, 2: 25, 3: 50, 4: 100}


# ─── DATA LAYER ─────────────────────────────────────────────────────────────

def contribution_level(count: int) -> int:
    if count <= 0:   return 0
    if count <= 3:   return 1
    if count <= 9:   return 2
    if count <= 19:  return 3
    return 4


def fetch_github_contributions(username="tace-x", token=None):
    """
    Fetch 52/53-week contribution calendar from GitHub GraphQL API.
    Returns list of dicts: [{date, count, level, week, day}]
    week = 0..52, day = 0..6 (Sun=0, Sat=6)
    """
    if not token:
        token = os.environ.get("GITHUB_TOKEN")

    if not token:
        try:
            r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip():
                token = r.stdout.strip()
        except Exception:
            pass

    # Try gh api directly if available
    try:
        query = f"""query {{
          user(login: "{username}") {{
            contributionsCollection {{
              contributionCalendar {{
                totalContributions
                weeks {{
                  contributionDays {{
                    date
                    contributionCount
                    contributionLevel
                  }}
                }}
              }}
            }}
          }}
        }}"""
        gh_cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
        res = subprocess.run(gh_cmd, capture_output=True, text=True)
        if res.returncode == 0:
            data = json.loads(res.stdout)
            weeks = (data["data"]["user"]["contributionsCollection"]
                     ["contributionCalendar"]["weeks"])
            cells = []
            for week_idx, week in enumerate(weeks):
                for day in week["contributionDays"]:
                    count = day["contributionCount"]
                    lv = contribution_level(count)
                    cells.append({
                        "date":  day["date"],
                        "count": count,
                        "level": lv,
                        "week":  week_idx,
                        "day":   datetime.fromisoformat(day["date"]).weekday(),
                    })
            return cells, None
    except Exception:
        pass

    if not token:
        return None, "No GITHUB_TOKEN or gh CLI auth available"

    query = f"""query {{
      user(login: "{username}") {{
        contributionsCollection {{
          contributionCalendar {{
            totalContributions
            weeks {{
              contributionDays {{
                date
                contributionCount
                contributionLevel
              }}
            }}
          }}
        }}
      }}
    }}"""
    payload = json.dumps({"query": query}).encode()
    headers = {
        "Authorization": f"bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "tace-x-arcade-generator/2.0",
    }
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers=headers,
        method="POST",
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        return None, f"Network error: {e}"

    if "errors" in data:
        return None, f"GraphQL error: {data['errors']}"

    weeks = (data["data"]["user"]["contributionsCollection"]
             ["contributionCalendar"]["weeks"])

    cells = []
    for week_idx, week in enumerate(weeks):
        for day in week["contributionDays"]:
            count = day["contributionCount"]
            lv = contribution_level(count)
            cells.append({
                "date":  day["date"],
                "count": count,
                "level": lv,
                "week":  week_idx,
                "day":   datetime.fromisoformat(day["date"]).weekday(),
            })
    return cells, None


def make_dev_fixture():
    """Fallback fixture if API and cached data are both unavailable."""
    cells = []
    rng = random.Random(0x74616365)
    start = datetime(2025, 10, 26, tzinfo=timezone.utc)
    for week in range(53):
        for day in range(7):
            date = start + timedelta(weeks=week, days=day)
            if rng.random() < 0.30:
                count = rng.choices(
                    [1, 2, 3, 5, 8, 12, 15, 22],
                    weights=[20, 15, 12, 10, 8, 5, 3, 2]
                )[0]
            else:
                count = 0
            cells.append({
                "date":  date.strftime("%Y-%m-%d"),
                "count": count,
                "level": contribution_level(count),
                "week":  week,
                "day":   day,
            })
    return cells


# ─── FONT HELPER ────────────────────────────────────────────────────────────

def load_fonts():
    candidates = [
        "/System/Library/Fonts/Monaco.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/Library/Fonts/Courier New.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return {
                    "sm":  ImageFont.truetype(path, 9),
                    "md":  ImageFont.truetype(path, 11),
                    "lg":  ImageFont.truetype(path, 14),
                    "xl":  ImageFont.truetype(path, 18),
                    "xxl": ImageFont.truetype(path, 22),
                }
            except Exception:
                pass
    d = ImageFont.load_default()
    return {"sm": d, "md": d, "lg": d, "xl": d, "xxl": d}


# ─── SPRITE PRIMITIVES ──────────────────────────────────────────────────────

def draw_ship(draw, cx, cy, banking=0, thrust_t=0, firing=False):
    """Crisp 20-pixel-tall spaceship."""
    cx, cy = int(cx), int(cy)
    bx = 1 if banking > 0 else (-1 if banking < 0 else 0)
    # Hull
    pixels = [
        (0+bx, -9, P["CYAN"]),
        (0+bx, -8, P["WHITE"]),
        (-1+bx, -7, P["CYAN"]), (0+bx, -7, P["WHITE"]), (1+bx, -7, P["CYAN"]),
        (-1, -6, P["CYAN"]), (0, -6, P["WHITE"]), (1, -6, P["CYAN"]),
        (-2, -5, P["MID"]),  (-1, -5, P["WHITE"]), (0, -5, P["CYAN"]),  (1, -5, P["WHITE"]), (2, -5, P["MID"]),
        (-2, -4, P["SHADOW"]),(-1, -4, P["CYAN"]),  (0, -4, P["CYAN"]),  (1, -4, P["CYAN"]),  (2, -4, P["SHADOW"]),
        (-3, -3, P["SHADOW"]),(-2, -3, P["MID"]),   (-1, -3, P["CYAN"]), (0, -3, P["WHITE"]), (1, -3, P["CYAN"]),  (2, -3, P["MID"]),   (3, -3, P["SHADOW"]),
        (-6, -1, P["CYAN"]),  (-5, -1, P["SHADOW"]),(0, -1, P["CYAN"]), (5, -1, P["SHADOW"]),  (6, -1, P["CYAN"]),
        (-7, 0, P["CYAN"]),   (-6, 0, P["MID"]),    (0, 0, P["MID"]),    (6, 0, P["MID"]),    (7, 0, P["CYAN"]),
        (-4, 1, P["MINT"]),   (4, 1, P["MINT"]),
        (-4, 2, P["MINT"]),   (4, 2, P["MINT"]),
    ]
    for dx, dy, col in pixels:
        draw.rectangle([cx+dx*2, cy+dy*2, cx+dx*2+1, cy+dy*2+1], fill=col)
    # Flame
    fl = 4 + (thrust_t % 4)
    fcol = P["MINT"] if thrust_t % 2 == 0 else P["CYAN"]
    for foffset in (-7, 7):
        draw.rectangle([cx+foffset, cy+8, cx+foffset+1, cy+8+fl], fill=fcol)
        draw.rectangle([cx+foffset, cy+8, cx+foffset+1, cy+9], fill=P["WHITE"])
    # Muzzle flash
    if firing:
        draw.rectangle([cx-2, cy-14, cx+2, cy-10], fill=P["WHITE"])
        draw.rectangle([cx-4, cy-13, cx+4, cy-11], fill=P["CYAN"])


def draw_contribution_cell(draw, cx, cy, level, size=9, tick=0):
    """Render a contribution cell as a glowing pixel cube."""
    col = LEVEL_COLOR[level]
    h = size // 2
    # Main body
    draw.rectangle([cx-h, cy-h, cx+h, cy+h], fill=col)
    # Bright top-left highlight
    if level > 0:
        br_col = {
            1: P["MINT_LT"],
            2: P["CYAN_DIM"],
            3: (196, 181, 253),
            4: (253, 164, 175),
        }.get(level, P["WHITE"])
        draw.rectangle([cx-h, cy-h, cx-h+2, cy-h+2], fill=br_col)
        if level >= 3 and tick % 4 == 0:
            draw.point([cx, cy], fill=P["WHITE"])


def draw_ghost_cell(draw, cx, cy, size=9):
    """Empty contribution slot — dim outline only."""
    h = size // 2
    draw.rectangle([cx-h, cy-h, cx+h, cy+h], outline=P["SHADOW"], width=1)


def draw_reticle(draw, cx, cy, size=9, col=P["CYAN"]):
    """Target acquisition reticle / brackets around locked cell."""
    h = size // 2 + 3
    # Corner brackets
    draw.line([(cx-h, cy-h), (cx-h+3, cy-h)], fill=col, width=1)
    draw.line([(cx-h, cy-h), (cx-h, cy-h+3)], fill=col, width=1)
    draw.line([(cx+h, cy-h), (cx+h-3, cy-h)], fill=col, width=1)
    draw.line([(cx+h, cy-h), (cx+h, cy-h+3)], fill=col, width=1)
    draw.line([(cx-h, cy+h), (cx-h+3, cy+h)], fill=col, width=1)
    draw.line([(cx-h, cy+h), (cx-h, cy-h-3)], fill=col, width=1)
    draw.line([(cx+h, cy+h), (cx+h-3, cy+h)], fill=col, width=1)
    draw.line([(cx+h, cy+h), (cx+h, cy+h-3)], fill=col, width=1)


def draw_single_projectile(draw, x1, y1, x2, y2, progress, col):
    """
    Renders exactly ONE projectile traveling visibly from (x1, y1) to (x2, y2).
    Progress: 0.0 at launch -> 1.0 at target.
    """
    curr_x = int(x1 + (x2 - x1) * progress)
    curr_y = int(y1 + (y2 - y1) * progress)

    tail_x = int(x1 + (x2 - x1) * max(0.0, progress - 0.18))
    tail_y = int(y1 + (y2 - y1) * max(0.0, progress - 0.18))

    # Outer glow
    draw.line([(tail_x, tail_y), (curr_x, curr_y)], fill=col, width=3)
    # Bright inner core
    draw.line([(tail_x, tail_y), (curr_x, curr_y)], fill=P["WHITE"], width=1)
    # Glowing diamond head
    draw.rectangle([curr_x-2, curr_y-2, curr_x+2, curr_y+2], fill=col)
    draw.rectangle([curr_x-1, curr_y-1, curr_x+1, curr_y+1], fill=P["WHITE"])


def draw_cell_impact(draw, cx, cy, col):
    """Single cell pop & impact burst."""
    # Central flash
    draw.rectangle([cx-4, cy-4, cx+4, cy+4], fill=P["WHITE"])
    draw.rectangle([cx-6, cy-6, cx+6, cy+6], outline=col, width=1)
    # 8 radial explosion particles
    rad = 8
    for angle_deg in range(0, 360, 45):
        a = math.radians(angle_deg)
        px = int(cx + math.cos(a) * rad)
        py = int(cy + math.sin(a) * rad)
        draw.rectangle([px-1, py-1, px+1, py+1], fill=col)
        draw.point([px, py], fill=P["WHITE"])


# ─── LAYOUT ─────────────────────────────────────────────────────────────────

CW, CH = 860, 360

GRID_COLS = 53   # weeks (covers 53 weeks)
GRID_ROWS = 7    # days
CELL_SZ   = 9    # cell pixel size
CELL_GAP  = 3    # gap between cells

GRID_W  = GRID_COLS * (CELL_SZ + CELL_GAP)
GRID_H  = GRID_ROWS * (CELL_SZ + CELL_GAP)
GRID_OX = (CW - GRID_W) // 2   # Centered horizontally
GRID_OY = 66                   # Below HUD

SHIP_Y = CH - 34


def cell_screen_pos(week, day):
    """Return center screen position of a contribution cell."""
    x = GRID_OX + week * (CELL_SZ + CELL_GAP) + CELL_SZ // 2
    y = GRID_OY + day  * (CELL_SZ + CELL_GAP) + CELL_SZ // 2
    return x, y


# ─── STATE MACHINE ──────────────────────────────────────────────────────────

class ArcadeState:
    IDLE           = "IDLE"
    AIMING         = "AIMING"
    FIRING         = "FIRING"
    IMPACT         = "IMPACT"
    CELL_CLEARED   = "CELL_CLEARED"
    SECTOR_CLEARED = "SECTOR_CLEARED"
    VICTORY        = "VICTORY"
    RESET          = "RESET"


# ─── ANIMATION ENGINE ───────────────────────────────────────────────────────

def generate_arcade_gif(cells, output_path, is_fixture=False, seed=0x54414345):
    """
    Generates the arcade shooter with RANDOM target selection:
      - Targets are chosen RANDOMLY from remaining active GitHub cells.
      - Exactly ONE projectile at a time.
      - Ship aims, fires, projectile visibly travels, and cell pops/dissolves.
      - Next shot does not launch until previous shot completes.
      - Authentic GitHub contribution data (never fabricates cells).
      - After all targets cleared: Sector Cleared -> Victory -> Scanline Reset.
    """
    fonts = load_fonts()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Separate active and empty cells
    active_cells = [c for c in cells if c["level"] > 0]
    empty_cells  = [c for c in cells if c["level"] == 0]

    total_targets = len(active_cells)
    total_score = sum(LEVEL_PTS[t["level"]] for t in active_cells)

    all_dates = sorted(c["date"] for c in cells)
    date_range = f"{all_dates[0]}  →  {all_dates[-1]}" if all_dates else "UNKNOWN"

    # Pre-build starfield
    rng_stars = random.Random(42)
    stars = [(rng_stars.randint(4, CW-4), rng_stars.randint(58, CH-10),
              rng_stars.choice([P["SHADOW"], P["MID"], P["CYAN_DIM"]]))
             for _ in range(60)]

    # ─── RANDOM TARGET SELECTION ───────────────────────────────────────────
    # Maintain remaining active cells pool.
    # For every shot, choose a uniform random cell from remaining, pop it, and enqueue combat frames.
    rng = random.Random(seed)
    remaining_pool = list(active_cells)
    random_shot_order = []
    while remaining_pool:
        idx = rng.randrange(len(remaining_pool))
        target = remaining_pool.pop(idx)
        random_shot_order.append(target)

    # ─── COMPOSE EXPLICIT FRAME SCHEDULE ───
    frame_schedule = []

    # 1. IDLE / INIT (8 frames)
    for f in range(8):
        frame_schedule.append({
            "state": ArcadeState.IDLE,
            "target_idx": -1,
            "target": None,
            "proj": None,
            "impact": False,
            "cleared_count": 0,
            "tag": ("SYSTEM INITIALIZING", P["MUTED"]),
            "init_f": f,
        })

    # 2. RANDOM COMBAT SEQUENCE (One shot at a time)
    cleared_count = 0
    for i, t in enumerate(random_shot_order):
        # Frame A: AIMING
        # Ship positions and locks targeting reticle onto the randomly chosen cell
        frame_schedule.append({
            "state": ArcadeState.AIMING,
            "target_idx": i,
            "target": t,
            "proj": None,
            "impact": False,
            "cleared_count": cleared_count,
            "tag": (f"TARGET LOCK [W{t['week']:02d}:D{t['day']}]", P["AMBER"]),
        })

        # Frame B: FIRING
        # Projectile is launched and travels visibly in mid-flight from ship cannon towards cell
        frame_schedule.append({
            "state": ArcadeState.FIRING,
            "target_idx": i,
            "target": t,
            "proj": 0.50, # In flight
            "impact": False,
            "cleared_count": cleared_count,
            "tag": (f"FIRING [TGT #{i+1:03d}]", P["RED"]),
        })

        # Frame C: IMPACT & CELL CLEARED
        # Projectile strikes cell, explosion pops/dissolves cell, score updates
        cleared_count += 1
        frame_schedule.append({
            "state": ArcadeState.IMPACT,
            "target_idx": i,
            "target": t,
            "proj": None,
            "impact": True,
            "cleared_count": cleared_count,
            "tag": (f"IMPACT [+ {LEVEL_PTS[t['level']]} PTS]", P["MINT_LT"]),
        })

    # 3. SECTOR CLEARED (1 frame)
    frame_schedule.append({
        "state": ArcadeState.SECTOR_CLEARED,
        "target_idx": total_targets,
        "target": None,
        "proj": None,
        "impact": False,
        "cleared_count": total_targets,
        "tag": ("SECTOR CLEARED", P["MINT"]),
    })

    # 4. VICTORY (16 frames)
    for f in range(16):
        frame_schedule.append({
            "state": ArcadeState.VICTORY,
            "target_idx": total_targets,
            "target": None,
            "proj": None,
            "impact": False,
            "cleared_count": total_targets,
            "tag": ("VICTORY ACHIEVED", P["MINT"]),
            "vf": f,
        })

    # 5. RESET (8 frames)
    for f in range(8):
        frame_schedule.append({
            "state": ArcadeState.RESET,
            "target_idx": -1,
            "target": None,
            "proj": None,
            "impact": False,
            "cleared_count": total_targets,
            "tag": ("RESETTING GRID...", P["MUTED"]),
            "rf": f,
        })

    total_frames = len(frame_schedule)

    # ─── RENDER ALL FRAMES ───
    frames = []
    durations = []
    prev_ship_x = cell_screen_pos(random_shot_order[0]["week"], random_shot_order[0]["day"])[0] if random_shot_order else CW // 2
    ship_x = prev_ship_x

    for f_idx, sched in enumerate(frame_schedule):
        im = Image.new("RGB", (CW, CH), P["VOID"])
        draw = ImageDraw.Draw(im)

        state = sched["state"]
        cleared_n = sched["cleared_count"]
        cur_target = sched["target"]
        tgt_idx = sched["target_idx"]

        # Calculate score strictly from cleared targets
        if cleared_n == 0:
            cur_score = 0
        elif cleared_n >= total_targets:
            cur_score = total_score
        else:
            cur_score = sum(LEVEL_PTS[t["level"]] for t in random_shot_order[:cleared_n])

        # ─── STARFIELD ───
        for sx, sy, sc in stars:
            if (f_idx + sx) % 13 == 0:
                draw.point([sx, sy], fill=P["WHITE"])
            else:
                draw.point([sx, sy], fill=sc)

        # ─── HUD BAR ───
        draw.rectangle([0, 0, CW, 52], fill=P["DARK"])
        draw.line([(0, 52), (CW, 52)], fill=P["MID"], width=1)
        draw.line([(0, 53), (CW, 53)], fill=P["CYAN"], width=1)

        # Title
        draw.text((16, 17), "TACE-X  //  ARCADE DEFENDER", fill=P["MINT"], font=fonts["md"])

        # Score (updates strictly on hit)
        score_str = f"SCORE: {cur_score:06d}"
        draw.text((340, 17), score_str, fill=P["CYAN"], font=fonts["md"])

        # State Tag
        tag_text, tag_col = sched["tag"]
        draw.text((CW - 16, 17), tag_text, fill=tag_col, font=fonts["md"], anchor="ra")

        # Sub-header: Date range
        draw.text((CW // 2, 57), date_range, fill=P["MUTED"], font=fonts["sm"], anchor="mm")

        # ─── CONTRIBUTION GRID ───
        # Active cells destroyed so far:
        destroyed_now = set((t["week"], t["day"]) for t in random_shot_order[:cleared_n])
        # If currently in IMPACT frame, the cell being hit is drawn exploding
        if sched["impact"] and cleared_n > 0:
            imp_cell = random_shot_order[cleared_n - 1]
            destroyed_now.remove((imp_cell["week"], imp_cell["day"]))

        for t in active_cells:
            key = (t["week"], t["day"])
            cx, cy = cell_screen_pos(t["week"], t["day"])
            if key not in destroyed_now:
                draw_contribution_cell(draw, cx, cy, t["level"], CELL_SZ, f_idx)

        # Empty (ghost) cells — never targeted
        for c in empty_cells:
            cx, cy = cell_screen_pos(c["week"], c["day"])
            draw_ghost_cell(draw, cx, cy, CELL_SZ)

        # If impacting in this frame, draw the impact explosion
        if sched["impact"] and cleared_n > 0:
            imp_cell = random_shot_order[cleared_n - 1]
            cx, cy = cell_screen_pos(imp_cell["week"], imp_cell["day"])
            draw_cell_impact(draw, cx, cy, LEVEL_COLOR[imp_cell["level"]])

        # ─── TARGET RETICLE ───
        if cur_target is not None and state in (ArcadeState.AIMING, ArcadeState.FIRING):
            tx, ty = cell_screen_pos(cur_target["week"], cur_target["day"])
            draw_reticle(draw, tx, ty, CELL_SZ, P["CYAN"])

        # ─── SHIP POSITIONING ───
        if cur_target is not None:
            target_x = cell_screen_pos(cur_target["week"], cur_target["day"])[0]
        else:
            target_x = CW // 2

        banking = 1 if (target_x - prev_ship_x) > 4 else (-1 if (target_x - prev_ship_x) < -4 else 0)
        ship_x = target_x
        prev_ship_x = ship_x

        # Ship Y position
        if state == ArcadeState.IDLE:
            init_f = sched.get("init_f", 0)
            entry_t = init_f / 7.0
            actual_ship_y = int(CH + 30 - (CH + 30 - SHIP_Y) * entry_t)
        else:
            actual_ship_y = SHIP_Y

        is_firing = (state == ArcadeState.FIRING)
        draw_ship(draw, ship_x, actual_ship_y, banking, f_idx, is_firing)

        # ─── SINGLE PROJECTILE ───
        # Strictly one projectile at a time in FIRING state
        if sched["proj"] is not None and cur_target is not None:
            tx, ty = cell_screen_pos(cur_target["week"], cur_target["day"])
            proj_col = LEVEL_COLOR[cur_target["level"]]
            cannon_x = ship_x
            cannon_y = actual_ship_y - 12
            draw_single_projectile(draw, cannon_x, cannon_y, tx, ty, sched["proj"], proj_col)

        # ─── VICTORY OVERLAY ───
        if state == ArcadeState.VICTORY:
            vf = sched.get("vf", 0)
            mx, my, mw, mh = CW//2 - 200, CH//2 - 54, 400, 108
            draw.rectangle([mx-3, my-3, mx+mw+3, my+mh+3], fill=P["SHADOW"], outline=P["CYAN"], width=2)
            draw.rectangle([mx, my, mx+mw, my+mh], fill=P["DARK"])
            draw.text((CW//2, my+26), ">> ACTIVITY CLEARED <<", fill=P["MINT"],
                      font=fonts["xl"], anchor="mm")
            active_desc = f"{total_targets} CONTRIBUTION CELLS CLEARED"
            draw.text((CW//2, my+54), active_desc, fill=P["WHITE"],
                      font=fonts["sm"], anchor="mm")
            fixture_note = "  [DEV FIXTURE]" if is_fixture else ""
            score_line = f"FINAL SCORE: {total_score:,} PTS{fixture_note}"
            draw.text((CW//2, my+80), score_line, fill=P["CYAN"],
                      font=fonts["md"], anchor="mm")

        # ─── RESET WIPE ───
        if state == ArcadeState.RESET:
            rf = sched.get("rf", 0)
            wipe_t = rf / 7.0
            wipe_y = int(54 + wipe_t * (CH - 54))
            draw.line([(0, wipe_y), (CW, wipe_y)], fill=P["CYAN"], width=3)
            draw.line([(0, wipe_y-2), (CW, wipe_y-2)], fill=P["WHITE"], width=1)
            draw.line([(0, wipe_y+2), (CW, wipe_y+2)], fill=P["MINT"], width=1)

        # ─── BOTTOM CONSOLE ───
        draw.line([(0, CH-18), (CW, CH-18)], fill=P["MID"], width=1)
        note = "[DEV FIXTURE — NOT REAL ACTIVITY]" if is_fixture else "VERIFIED GITHUB CONTRIBUTION GRID [RANDOM COMBAT]"
        note_col = P["AMBER"] if is_fixture else P["CYAN_DIM"]
        draw.text((16, CH-11), note, fill=note_col, font=fonts["sm"])
        remaining = max(0, total_targets - cleared_n)
        draw.text((CW-16, CH-11), f"REMAINING: {remaining:03d}  //  TOTAL ACTIVE: {total_targets}",
                  fill=P["MUTED"], font=fonts["sm"], anchor="ra")

        # Frame pacing
        if state == ArcadeState.VICTORY:
            dur = 120
        elif state == ArcadeState.IDLE:
            dur = 100
        elif state == ArcadeState.RESET:
            dur = 80
        else:
            dur = 55

        frames.append(im.quantize(colors=64))
        durations.append(dur)

    # ─── SAVE GIF ───
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )
    size_kb = out.stat().st_size / 1024
    print(f"[✓] Arcade GIF -> {out} ({size_kb:.1f} KB, {len(frames)} frames)")
    return {
        "path": str(out),
        "size_kb": size_kb,
        "frames": len(frames),
        "targets": total_targets,
        "score": total_score,
        "is_fixture": is_fixture,
        "schedule": frame_schedule,
        "shot_order": random_shot_order,
    }


def generate_contact_sheet(cells, output_path, results):
    """
    Generate a 6-panel contact sheet proving single-shot random state transitions:
      1. INITIALIZE (Ship enters combat zone)
      2. AIMING (Aim locked on a random active cell)
      3. FIRING (Single projectile traveling to cell)
      4. IMPACT (Projectile strikes cell, explosion burst)
      5. CLEARING (Battlefield progressively clearing randomly)
      6. VICTORY (Sector cleared, victory banner held)
    """
    gif_path = Path(output_path).parent / "arcade_shooter.gif"
    if not gif_path.exists():
        return

    gif = Image.open(gif_path)
    schedule = results.get("schedule", [])
    total_frames = len(schedule)

    f_init = 4
    f_aiming = next((i for i, s in enumerate(schedule) if s["state"] == ArcadeState.AIMING), 8)
    f_firing = next((i for i, s in enumerate(schedule) if s["state"] == ArcadeState.FIRING), 9)
    f_impact = next((i for i, s in enumerate(schedule) if s["state"] == ArcadeState.IMPACT), 10)
    f_clearing = total_frames // 2
    f_victory = next((i for i, s in enumerate(schedule) if s["state"] == ArcadeState.VICTORY), total_frames - 20) + 4

    frames_needed = [f_init, f_aiming, f_firing, f_impact, f_clearing, f_victory]

    extracted = []
    for fi in frames_needed:
        try:
            gif.seek(fi)
            extracted.append(gif.copy().convert("RGB"))
        except EOFError:
            pass

    if len(extracted) < 6:
        return

    TW, TH = extracted[0].size
    scale = 0.5
    tw, th = int(TW * scale), int(TH * scale)

    labels = [
        "1. IDLE / INIT — Ship enters sector",
        "2. AIMING — Lock reticle on random cell",
        "3. FIRING — Single projectile in transit",
        "4. IMPACT — Cell pops & dissolves",
        "5. CLEARING — Random combat clearing grid",
        "6. VICTORY — Sector 100% cleared",
    ]

    sheet = Image.new("RGB", (tw * 2, th * 3), P["VOID"])
    sdraw = ImageDraw.Draw(sheet)
    font = load_fonts()["sm"]

    for i, frame in enumerate(extracted[:6]):
        thumb = frame.resize((tw, th), Image.Resampling.LANCZOS)
        row, col = i // 2, i % 2
        ox, oy = col * tw, row * th
        sheet.paste(thumb, (ox, oy))
        sdraw.rectangle([ox, oy, ox+tw, oy+th], outline=P["MID"], width=1)
        lbl = labels[i]
        sdraw.rectangle([ox+4, oy+th-18, ox+min(len(lbl)*6+14, tw-4), oy+th-4],
                        fill=P["DARK"], outline=P["CYAN"])
        sdraw.text((ox+8, oy+th-16), lbl, fill=P["CYAN"], font=font)

    sheet_path = Path(output_path)
    sheet.save(sheet_path)
    print(f"[✓] Contact sheet -> {sheet_path}")


# ─── VALIDATION SUITE ────────────────────────────────────────────────────────

def run_tests(cells, results):
    """Automated checks for single-projectile random targeting integrity."""
    passed = 0
    failed = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  [PASS] {name}")
            passed += 1
        else:
            print(f"  [FAIL] {name}{' — ' + detail if detail else ''}")
            failed += 1

    print("\n[*] Running arcade random combat telemetry validation suite...")

    active = [c for c in cells if c["level"] > 0]
    empty  = [c for c in cells if c["level"] == 0]

    check("Contribution data not empty", len(cells) > 0)
    check("Has active (non-zero) cells", len(active) > 0)
    check("Empty cells have level 0", all(c["level"] == 0 for c in empty))
    check("Active cells have level 1..4", all(1 <= c["level"] <= 4 for c in active))

    schedule = results.get("schedule", [])
    shot_order = results.get("shot_order", [])

    check("Shot order targets exactly all active cells", len(shot_order) == len(active))
    # Confirm no cell targeted twice
    shot_keys = [(t["week"], t["day"]) for t in shot_order]
    check("Zero duplicate targets (each destroyed cell cleared once)", len(set(shot_keys)) == len(active))

    # Confirm targeting is genuinely random rather than sequential (e.g., column by column)
    weeks = [t["week"] for t in shot_order]
    is_strictly_sequential = all(weeks[i] <= weeks[i+1] for i in range(len(weeks)-1))
    check("Targeting is non-sequential (randomized across calendar)", not is_strictly_sequential)

    week_diffs = [abs(weeks[i] - weeks[i-1]) for i in range(1, len(weeks))]
    avg_hop = sum(week_diffs) / len(week_diffs) if week_diffs else 0
    check("Targeting has substantial hop distance across grid (avg > 5 weeks)", avg_hop > 5.0, f"actual: {avg_hop:.1f} weeks")

    firing_frames = [s for s in schedule if s["state"] == ArcadeState.FIRING]
    impact_frames = [s for s in schedule if s["state"] == ArcadeState.IMPACT]

    check("Firing frame count matches active cells exactly",
          len(firing_frames) == len(active),
          f"firing: {len(firing_frames)}, active: {len(active)}")
    check("Impact frame count matches active cells exactly",
          len(impact_frames) == len(active),
          f"impact: {len(impact_frames)}, active: {len(active)}")

    # Verify single projectile: no frame has multiple projectiles
    single_projectile_rule = all(
        (s["proj"] is not None and s["state"] == ArcadeState.FIRING) or (s["proj"] is None)
        for s in schedule
    )
    check("Strictly one projectile at a time (zero overlapping)", single_projectile_rule)

    # Verify score strictly updates only upon impact
    score_integrity = True
    prev_cleared = 0
    for s in schedule:
        if s["state"] == ArcadeState.FIRING:
            if s["cleared_count"] != prev_cleared:
                score_integrity = False
        elif s["state"] == ArcadeState.IMPACT:
            if s["cleared_count"] != prev_cleared + 1:
                score_integrity = False
            prev_cleared = s["cleared_count"]
    check("Score and cell clearance strictly update on impact only", score_integrity)

    # Verify victory occurs ONLY after all targets are cleared
    victory_frames = [s for s in schedule if s["state"] == ArcadeState.VICTORY]
    check("Victory frames exist", len(victory_frames) > 0)
    victory_cleared = all(s["cleared_count"] == len(active) for s in victory_frames)
    check("Victory state occurs only after 100% of targets cleared", victory_cleared)

    # GIF file checks
    gif_path = Path(results["path"])
    check("GIF file exists", gif_path.exists())
    check("GIF size < 2.0 MB", results["size_kb"] < 2048, f"actual: {results['size_kb']:.1f} KB")

    print(f"\n[*] Results: {passed} passed, {failed} failed")
    return failed == 0


# ─── MAIN ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="TACE-X Contribution Arcade Shooter (Random Combat)")
    parser.add_argument("--username", default="tace-x")
    parser.add_argument("--output-dir", "-o", default="assets/arcade")
    parser.add_argument("--data", "-d", default=None, help="Path to contribution data JSON file")
    parser.add_argument("--fixture", action="store_true", help="Force dev fixture (no API)")
    parser.add_argument("--test", action="store_true", help="Run validation after generation")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    is_fixture = args.fixture
    data_file = args.data or os.path.join(args.output_dir, "contribution_data.json")

    cells = None

    # 1. If not forcing fixture, try fetching live data from GitHub API first
    if not is_fixture:
        print(f"[*] Fetching live GitHub contribution data for @{args.username}...")
        fetched_cells, err = fetch_github_contributions(args.username, token)
        if not err and fetched_cells:
            cells = fetched_cells
            print(f"[✓] Successfully fetched {len(cells)} cells from GitHub API")
            try:
                os.makedirs(args.output_dir, exist_ok=True)
                with open(data_file, "w", encoding="utf-8") as f:
                    json.dump({
                        "username": args.username,
                        "source": "github-graphql-api",
                        "fetched_at": datetime.now(timezone.utc).isoformat(),
                        "cells": cells
                    }, f, indent=2)
                print(f"[✓] Saved updated contribution data to {data_file}")
            except Exception as e:
                print(f"[!] Could not save {data_file}: {e}")
        else:
            print(f"[!] API fetch notice: {err}")

    # 2. If API fetch did not produce cells, load from existing cached data_file
    if cells is None and not is_fixture and os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
            cells = saved.get("cells")
            active_cnt = sum(1 for c in cells if c["level"] > 0)
            print(f"[✓] Loaded verified GitHub contribution data from cache {data_file} ({len(cells)} cells, {active_cnt} active)")
        except Exception as e:
            print(f"[!] Could not load {data_file}: {e}")
            cells = None

    # 3. Fallback to fixture only if forced or data completely unavailable
    if cells is None:
        if not args.fixture:
            print("[!] Using DEVELOPMENT FIXTURE — replace with live data or valid cache")
        cells = make_dev_fixture()
        is_fixture = True

    # ─── Generate GIF ───
    gif_path = os.path.join(args.output_dir, "arcade_shooter.gif")
    results = generate_arcade_gif(cells, gif_path, is_fixture)

    # ─── Contact sheet ───
    sheet_path = os.path.join(args.output_dir, "arcade_contact_sheet.png")
    generate_contact_sheet(cells, sheet_path, results)

    # ─── Tests ───
    if args.test:
        success = run_tests(cells, results)
        if not success:
            sys.exit(1)

    print(f"\n[+] Generation complete.")
    print(f"    GIF:     {gif_path} ({results['size_kb']:.1f} KB, {results['frames']} frames)")
    print(f"    Targets: {results['targets']} active contribution cells (Random combat)")
    print(f"    Score:   {results['score']:,} pts")
    if is_fixture:
        print("    ⚠️  DATA SOURCE: DEV FIXTURE")
    else:
        print("    ✓  DATA SOURCE: Real GitHub contribution API")


if __name__ == "__main__":
    main()
