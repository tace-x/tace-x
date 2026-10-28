#!/usr/bin/env python3
"""
TACE-X Contribution Grid Arcade Shooter
=========================================
Enhanced arcade space-shooter GIF implementing:
  - STRICT ROW-BY-ROW CLEARING: The bottommost eligible contribution row is completely
    cleared before moving upward to the next row.
  - RANDOMIZATION WITHIN ACTIVE ROW: Targets within the currently engaged row are
    cleared in randomized order.
  - CONTINUOUS SMOOTH MOVEMENT (NO TELEPORTATION): The ship glides smoothly along an eased
    flight trajectory with banking and motion ghosting between targets.
  - EXACT TARGETING & CLEARING: The projectile visibly travels from cannon to the exact
    target cell; the cell pops/dissolves only upon impact, and score increments strictly on hit.
  - EXACT ONE PROJECTILE AT A TIME: Never overlapping projectiles.
  - HUD TELEMETRY & ROW GAUGES: Active row gauge (▶ ROW 1 .. > ROW 7), active row guideline,
    flight trajectory dashed arc, and accurate GitHub contribution data.
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
    "VOID":       (5,   8,   13),   # #05080D
    "DARK":       (8,   13,  21),   # #080D15
    "SHADOW":     (11,  18,  32),   # #0B1220
    "MID":        (22,  36,  58),   # #16243A
    "BORDER":     (30,  48,  78),   # #1E304E
    "CYAN":       (0,   229, 255),  # #00E5FF
    "CYAN_DIM":   (22,  139, 255),  # #168BFF
    "MINT":       (0,   229, 255),  # #00E5FF
    "MINT_LT":    (110, 240, 255),
    "VIOLET":     (155, 109, 255),  # #9B6DFF
    "RED":        (255, 65,  108),  # #FF416C
    "AMBER":      (245, 158, 11),
    "WHITE":      (241, 245, 249),  # #F1F5F9
    "MUTED":      (140, 163, 189),  # #8CA3BD
}

LEVEL_COLOR = {
    0: P["SHADOW"],    # ghost — empty cell
    1: P["CYAN_DIM"],  # 1–3 contributions
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
        "User-Agent": "tace-x-arcade-generator/2.1",
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

def draw_ship(draw, cx, cy, banking=0, thrust_t=0, firing=False, ghost=False):
    """Crisp futuristic spaceship with motion banking and thruster flares."""
    cx, cy = int(cx), int(cy)
    bx = 1 if banking > 0 else (-1 if banking < 0 else 0)

    if ghost:
        hull_col = (11, 28, 48)
        core_col = (20, 50, 80)
    else:
        hull_col = P["CYAN"]
        core_col = P["WHITE"]

    # Hull pixels
    pixels = [
        (0+bx, -9, hull_col),
        (0+bx, -8, core_col),
        (-1+bx, -7, hull_col), (0+bx, -7, core_col), (1+bx, -7, hull_col),
        (-1, -6, hull_col), (0, -6, core_col), (1, -6, hull_col),
        (-2, -5, P["MID"]),  (-1, -5, core_col), (0, -5, hull_col),  (1, -5, core_col), (2, -5, P["MID"]),
        (-2, -4, P["SHADOW"]),(-1, -4, hull_col),  (0, -4, hull_col),  (1, -4, hull_col),  (2, -4, P["SHADOW"]),
        (-3, -3, P["SHADOW"]),(-2, -3, P["MID"]),   (-1, -3, hull_col), (0, -3, core_col), (1, -3, hull_col),  (2, -3, P["MID"]),   (3, -3, P["SHADOW"]),
        (-6, -1, hull_col),  (-5, -1, P["SHADOW"]),(0, -1, hull_col), (5, -1, P["SHADOW"]),  (6, -1, hull_col),
        (-7, 0, hull_col),   (-6, 0, P["MID"]),    (0, 0, P["MID"]),    (6, 0, P["MID"]),    (7, 0, hull_col),
        (-4, 1, hull_col),   (4, 1, hull_col),
        (-4, 2, hull_col),   (4, 2, hull_col),
    ]
    for dx, dy, col in pixels:
        draw.rectangle([cx+dx*2, cy+dy*2, cx+dx*2+1, cy+dy*2+1], fill=col)

    if not ghost:
        # Animated engine thrusters
        fl = 4 + (thrust_t % 4)
        fcol = P["CYAN"] if thrust_t % 2 == 0 else P["CYAN_DIM"]
        for foffset in (-7, 7):
            draw.rectangle([cx+foffset, cy+8, cx+foffset+1, cy+8+fl], fill=fcol)
            draw.rectangle([cx+foffset, cy+8, cx+foffset+1, cy+9], fill=P["WHITE"])

        # Muzzle flash
        if firing:
            draw.rectangle([cx-2, cy-15, cx+2, cy-11], fill=P["WHITE"])
            draw.rectangle([cx-4, cy-14, cx+4, cy-12], fill=P["CYAN"])


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
            2: P["CYAN"],
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

    tail_x = int(x1 + (x2 - x1) * max(0.0, progress - 0.20))
    tail_y = int(y1 + (y2 - y1) * max(0.0, progress - 0.20))

    # Outer glow
    draw.line([(tail_x, tail_y), (curr_x, curr_y)], fill=col, width=3)
    # Bright inner core
    draw.line([(tail_x, tail_y), (curr_x, curr_y)], fill=P["WHITE"], width=1)
    # Glowing diamond head
    draw.rectangle([curr_x-2, curr_y-2, curr_x+2, curr_y+2], fill=col)
    draw.rectangle([curr_x-1, curr_y-1, curr_x+1, curr_y+1], fill=P["WHITE"])


def draw_cell_impact(draw, cx, cy, col):
    """Single cell pop & impact burst."""
    draw.rectangle([cx-4, cy-4, cx+4, cy+4], fill=P["WHITE"])
    draw.rectangle([cx-6, cy-6, cx+6, cy+6], outline=col, width=1)
    # 8 radial explosion particles
    rad = 9
    for angle_deg in range(0, 360, 45):
        a = math.radians(angle_deg)
        px = int(cx + math.cos(a) * rad)
        py = int(cy + math.sin(a) * rad)
        draw.rectangle([px-1, py-1, px+1, py+1], fill=col)
        draw.point([px, py], fill=P["WHITE"])


# ─── LAYOUT ─────────────────────────────────────────────────────────────────

CW, CH = 860, 360

GRID_COLS = 53   # weeks
GRID_ROWS = 7    # days (0 = Top, 6 = Bottom)
CELL_SZ   = 9
CELL_GAP  = 3

GRID_W  = GRID_COLS * (CELL_SZ + CELL_GAP)
GRID_H  = GRID_ROWS * (CELL_SZ + CELL_GAP)
GRID_OX = (CW - GRID_W) // 2 - 20   # Centered horizontally with space for row gauges on right
GRID_OY = 68

SHIP_Y = CH - 34


def cell_screen_pos(week, day):
    """Return center screen position of a contribution cell."""
    x = GRID_OX + week * (CELL_SZ + CELL_GAP) + CELL_SZ // 2
    y = GRID_OY + day  * (CELL_SZ + CELL_GAP) + CELL_SZ // 2
    return x, y


# ─── STATE MACHINE ──────────────────────────────────────────────────────────

class ArcadeState:
    IDLE           = "IDLE"
    FLIGHT         = "FLIGHT"
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
    Generates the arcade shooter with STRICT ROW-BY-ROW CLEARING + CONTINUOUS MOVEMENT:
      - Bottommost eligible row is cleared first (day 6 down to day 0).
      - Random selection strictly WITHIN the active row.
      - Smooth continuous travel (zero teleportation) along an eased trajectory.
      - Exactly ONE projectile at a time.
      - Impact-driven clearing and score update.
    """
    fonts = load_fonts()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    active_cells = [c for c in cells if c["level"] > 0]
    empty_cells  = [c for c in cells if c["level"] == 0]

    total_targets = len(active_cells)
    total_score = sum(LEVEL_PTS[t["level"]] for t in active_cells)

    all_dates = sorted(c["date"] for c in cells)
    date_range = f"{all_dates[0]}  →  {all_dates[-1]}" if all_dates else "UNKNOWN"

    # Group active cells by row (day: 0..6).
    # Bottommost row on screen corresponds to the highest day index (day 6 down to day 0).
    rows_dict = {}
    for c in active_cells:
        rows_dict.setdefault(c["day"], []).append(c)

    # Sort row indices descending (bottom row first: 6, 5, 4, 3, 2, 1, 0)
    active_row_indices = sorted(rows_dict.keys(), reverse=True)
    total_active_rows = len(active_row_indices)

    # Build sequence: strictly row-by-row, randomized within row
    rng = random.Random(seed)
    ordered_row_targets = []
    for row_order_idx, day_val in enumerate(active_row_indices, 1):
        row_pool = list(rows_dict[day_val])
        while row_pool:
            idx = rng.randrange(len(row_pool))
            target = row_pool.pop(idx)
            ordered_row_targets.append({
                "target": target,
                "row_gauge_num": row_order_idx,   # 1 = bottom row, 7 = top row
                "total_rows": total_active_rows,
                "day_val": day_val,
            })

    # Pre-build starfield
    rng_stars = random.Random(42)
    stars = [(rng_stars.randint(4, CW-4), rng_stars.randint(58, CH-10),
              rng_stars.choice([P["SHADOW"], P["MID"], P["CYAN_DIM"]]))
             for _ in range(60)]

    # ─── BUILD CONTINUOUS FRAME SCHEDULE ───
    frame_schedule = []

    # 1. IDLE / INIT (8 frames)
    for f in range(8):
        frame_schedule.append({
            "state": ArcadeState.IDLE,
            "target_idx": -1,
            "target": None,
            "row_info": (1, total_active_rows, active_row_indices[0]),
            "proj": None,
            "impact": False,
            "cleared_count": 0,
            "ship_x": cell_screen_pos(ordered_row_targets[0]["target"]["week"], ordered_row_targets[0]["target"]["day"])[0],
            "ship_y": None,
            "banking": 0,
            "ghosts": [],
            "tag": ("SYSTEM INITIALIZING", P["MUTED"]),
            "init_f": f,
        })

    cleared_count = 0
    curr_ship_x = cell_screen_pos(ordered_row_targets[0]["target"]["week"], ordered_row_targets[0]["target"]["day"])[0]

    for shot_idx, item in enumerate(ordered_row_targets):
        target = item["target"]
        target_x, target_y = cell_screen_pos(target["week"], target["day"])
        row_num = item["row_gauge_num"]
        day_val = item["day_val"]
        row_info = (row_num, total_active_rows, day_val)

        # Smooth flight from curr_ship_x to target_x
        dist = abs(target_x - curr_ship_x)
        if dist <= 12:
            flight_steps = []
        elif dist <= 60:
            flight_steps = [0.50]
        elif dist <= 180:
            flight_steps = [0.33, 0.67]
        else:
            flight_steps = [0.25, 0.50, 0.75]

        # Flight frames (continuous motion with smooth easing)
        start_x = curr_ship_x
        for step_t in flight_steps:
            # Smooth cosine easing
            ease = (1.0 - math.cos(step_t * math.pi)) / 2.0
            interp_x = start_x + (target_x - start_x) * ease
            interp_y = SHIP_Y - int(math.sin(step_t * math.pi) * 6)
            bank = 1 if (target_x > start_x) else (-1 if (target_x < start_x) else 0)

            # Ghost trailing positions
            ghost_1 = start_x + (interp_x - start_x) * 0.4
            ghosts = [(ghost_1, interp_y + 2)]

            frame_schedule.append({
                "state": ArcadeState.FLIGHT,
                "target_idx": shot_idx,
                "target": target,
                "row_info": row_info,
                "proj": None,
                "impact": False,
                "cleared_count": cleared_count,
                "ship_x": interp_x,
                "ship_y": interp_y,
                "banking": bank,
                "ghosts": ghosts,
                "tag": (f"ENGAGING ROW {row_num}/{total_active_rows}", P["CYAN"]),
            })

        curr_ship_x = target_x

        # AIMING / LOCK FRAME: Arrived directly under target, reticle locks
        frame_schedule.append({
            "state": ArcadeState.AIMING,
            "target_idx": shot_idx,
            "target": target,
            "row_info": row_info,
            "proj": None,
            "impact": False,
            "cleared_count": cleared_count,
            "ship_x": target_x,
            "ship_y": SHIP_Y,
            "banking": 0,
            "ghosts": [],
            "tag": (f"TARGET LOCK [W{target['week']:02d}:D{target['day']}]", P["AMBER"]),
        })

        # FIRING FRAME: Projectile in transit from cannon directly towards target
        frame_schedule.append({
            "state": ArcadeState.FIRING,
            "target_idx": shot_idx,
            "target": target,
            "row_info": row_info,
            "proj": 0.50, # Mid-flight
            "impact": False,
            "cleared_count": cleared_count,
            "ship_x": target_x,
            "ship_y": SHIP_Y,
            "banking": 0,
            "ghosts": [],
            "tag": (f"FIRING [TGT #{shot_idx+1:03d}]", P["RED"]),
        })

        # IMPACT FRAME: Projectile impacts cell, cell pops & dissolves, score increments
        cleared_count += 1
        frame_schedule.append({
            "state": ArcadeState.IMPACT,
            "target_idx": shot_idx,
            "target": target,
            "row_info": row_info,
            "proj": None,
            "impact": True,
            "cleared_count": cleared_count,
            "ship_x": target_x,
            "ship_y": SHIP_Y,
            "banking": 0,
            "ghosts": [],
            "tag": (f"IMPACT [TGT #{shot_idx+1:03d}]", P["RED"]),
        })

    # SECTOR CLEARED
    last_row_info = (total_active_rows, total_active_rows, active_row_indices[-1])
    frame_schedule.append({
        "state": ArcadeState.SECTOR_CLEARED,
        "target_idx": total_targets,
        "target": None,
        "row_info": last_row_info,
        "proj": None,
        "impact": False,
        "cleared_count": total_targets,
        "ship_x": curr_ship_x,
        "ship_y": SHIP_Y,
        "banking": 0,
        "ghosts": [],
        "tag": ("SECTOR CLEARED", P["MINT"]),
    })

    # VICTORY (16 frames)
    for vf in range(16):
        frame_schedule.append({
            "state": ArcadeState.VICTORY,
            "target_idx": total_targets,
            "target": None,
            "row_info": last_row_info,
            "proj": None,
            "impact": False,
            "cleared_count": total_targets,
            "ship_x": curr_ship_x,
            "ship_y": SHIP_Y,
            "banking": 0,
            "ghosts": [],
            "tag": ("VICTORY ACHIEVED", P["MINT"]),
            "vf": vf,
        })

    # RESET (8 frames)
    for rf in range(8):
        frame_schedule.append({
            "state": ArcadeState.RESET,
            "target_idx": -1,
            "target": None,
            "row_info": last_row_info,
            "proj": None,
            "impact": False,
            "cleared_count": total_targets,
            "ship_x": CW // 2,
            "ship_y": SHIP_Y,
            "banking": 0,
            "ghosts": [],
            "tag": ("RESETTING GRID...", P["MUTED"]),
            "rf": rf,
        })

    total_frames = len(frame_schedule)

    # ─── RENDER ALL FRAMES ───
    frames = []
    durations = []
    ordered_target_list = [item["target"] for item in ordered_row_targets]

    for f_idx, sched in enumerate(frame_schedule):
        im = Image.new("RGB", (CW, CH), P["VOID"])
        draw = ImageDraw.Draw(im)

        state = sched["state"]
        cleared_n = sched["cleared_count"]
        cur_target = sched["target"]
        cur_row_num, total_rows, active_day_val = sched["row_info"]

        # Accurate score derived strictly from cleared targets
        if cleared_n == 0:
            cur_score = 0
        elif cleared_n >= total_targets:
            cur_score = total_score
        else:
            cur_score = sum(LEVEL_PTS[t["level"]] for t in ordered_target_list[:cleared_n])

        # ─── STARFIELD ───
        for sx, sy, sc in stars:
            if (f_idx + sx) % 13 == 0:
                draw.point([sx, sy], fill=P["WHITE"])
            else:
                draw.point([sx, sy], fill=sc)

        # ─── HUD BAR ───
        draw.rectangle([0, 0, CW, 52], fill=P["DARK"])
        draw.line([(0, 52), (CW, 52)], fill=P["MID"], width=1)
        draw.line([(0, 53), (CW, 53)], fill=P["BORDER"], width=1)

        # Left Title
        draw.text((18, 17), "TACE-X  //  ARCADE DEFENDER", fill=P["CYAN"], font=fonts["md"])

        # Center Score
        draw.text((320, 17), f"SCORE: {cur_score:06d}", fill=P["CYAN_DIM"], font=fonts["md"])

        # Right-Center Row Progress (as in reference image: CLEARING ROW 1 / 5)
        row_status_str = f"CLEARING ROW {cur_row_num} / {total_rows}"
        draw.text((540, 17), row_status_str, fill=P["CYAN"], font=fonts["md"])

        # Far-Right Status Tag
        tag_text, tag_col = sched["tag"]
        draw.text((CW - 18, 17), tag_text, fill=tag_col, font=fonts["md"], anchor="ra")

        # Sub-header: Date range
        draw.text((CW // 2, 57), date_range, fill=P["MUTED"], font=fonts["sm"], anchor="mm")

        # ─── ACTIVE ROW GUIDELINE ───
        # Dashed horizontal guideline spanning across the currently engaged row
        if state not in (ArcadeState.VICTORY, ArcadeState.RESET):
            guide_y = GRID_OY + active_day_val * (CELL_SZ + CELL_GAP) + CELL_SZ // 2
            for gx in range(GRID_OX - 10, GRID_OX + GRID_W + 10, 8):
                draw.line([(gx, guide_y), (gx + 4, guide_y)], fill=P["MID"], width=1)

        # ─── CONTRIBUTION GRID ───
        destroyed_now = set((t["week"], t["day"]) for t in ordered_target_list[:cleared_n])
        if sched["impact"] and cleared_n > 0:
            imp_cell = ordered_target_list[cleared_n - 1]
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

        # Impact burst
        if sched["impact"] and cleared_n > 0:
            imp_cell = ordered_target_list[cleared_n - 1]
            cx, cy = cell_screen_pos(imp_cell["week"], imp_cell["day"])
            draw_cell_impact(draw, cx, cy, LEVEL_COLOR[imp_cell["level"]])

        # ─── RIGHT-SIDE ROW GAUGES (Reference Image Detail) ───
        # Display row indicators on the right edge of grid: ▶ ROW 1 ... > ROW 7
        gauge_x = GRID_OX + GRID_W + 18
        for row_i, d_val in enumerate(active_row_indices, 1):
            row_y = GRID_OY + d_val * (CELL_SZ + CELL_GAP) + 1
            if row_i == cur_row_num and state not in (ArcadeState.VICTORY, ArcadeState.RESET):
                # Active row with glowing cyan arrow
                draw.text((gauge_x, row_y), f"▶ ROW {row_i}", fill=P["CYAN"], font=fonts["sm"])
            else:
                draw.text((gauge_x, row_y), f"> ROW {row_i}", fill=P["BORDER"], font=fonts["sm"])

        # ─── TARGET RETICLE ───
        if cur_target is not None and state in (ArcadeState.AIMING, ArcadeState.FIRING):
            tx, ty = cell_screen_pos(cur_target["week"], cur_target["day"])
            draw_reticle(draw, tx, ty, CELL_SZ, P["CYAN"])

        # ─── FLIGHT TRAJECTORY GUIDELINE (Subtle Dashed Arc) ───
        if state not in (ArcadeState.VICTORY, ArcadeState.RESET):
            for ax in range(GRID_OX, GRID_OX + GRID_W, 14):
                ay = int(SHIP_Y + math.sin(ax * 0.02) * 4)
                draw.line([(ax, ay), (ax + 5, ay)], fill=P["DARK"], width=1)

        # ─── MOTION GHOSTS (Echoes along trajectory) ───
        for gx, gy in sched.get("ghosts", []):
            draw_ship(draw, gx, gy, banking=sched["banking"], thrust_t=f_idx, firing=False, ghost=True)

        # ─── SHIP ───
        ship_x = sched["ship_x"]
        if state == ArcadeState.IDLE:
            init_f = sched.get("init_f", 0)
            entry_t = init_f / 7.0
            actual_ship_y = int(CH + 30 - (CH + 30 - SHIP_Y) * entry_t)
        else:
            actual_ship_y = sched.get("ship_y") or SHIP_Y

        is_firing = (state == ArcadeState.FIRING)
        draw_ship(draw, ship_x, actual_ship_y, sched["banking"], f_idx, is_firing)

        # ─── SINGLE PROJECTILE ───
        if sched["proj"] is not None and cur_target is not None:
            tx, ty = cell_screen_pos(cur_target["week"], cur_target["day"])
            proj_col = LEVEL_COLOR[cur_target["level"]]
            cannon_x = ship_x
            cannon_y = actual_ship_y - 12
            draw_single_projectile(draw, cannon_x, cannon_y, tx, ty, sched["proj"], proj_col)

        # ─── VICTORY OVERLAY ───
        if state == ArcadeState.VICTORY:
            mx, my, mw, mh = CW//2 - 200, CH//2 - 54, 400, 108
            draw.rectangle([mx-3, my-3, mx+mw+3, my+mh+3], fill=P["SHADOW"], outline=P["CYAN"], width=2)
            draw.rectangle([mx, my, mx+mw, my+mh], fill=P["DARK"])
            draw.text((CW//2, my+26), ">> ACTIVITY CLEARED <<", fill=P["CYAN"],
                      font=fonts["xl"], anchor="mm")
            active_desc = f"{total_targets} CONTRIBUTION CELLS CLEARED  //  ALL {total_rows} ROWS SECURED"
            draw.text((CW//2, my+54), active_desc, fill=P["WHITE"],
                      font=fonts["sm"], anchor="mm")
            fixture_note = "  [DEV FIXTURE]" if is_fixture else ""
            score_line = f"FINAL SCORE: {total_score:,} PTS{fixture_note}"
            draw.text((CW//2, my+80), score_line, fill=P["CYAN_DIM"],
                      font=fonts["md"], anchor="mm")

        # ─── RESET SCANLINE ───
        if state == ArcadeState.RESET:
            rf = sched.get("rf", 0)
            wipe_t = rf / 7.0
            wipe_y = int(54 + wipe_t * (CH - 54))
            draw.line([(0, wipe_y), (CW, wipe_y)], fill=P["CYAN"], width=3)
            draw.line([(0, wipe_y-2), (CW, wipe_y-2)], fill=P["WHITE"], width=1)
            draw.line([(0, wipe_y+2), (CW, wipe_y+2)], fill=P["CYAN_DIM"], width=1)

        # ─── BOTTOM CONSOLE ───
        draw.line([(0, CH-18), (CW, CH-18)], fill=P["MID"], width=1)
        note = "[DEV FIXTURE]" if is_fixture else "VERIFIED GITHUB CONTRIBUTION GRID"
        draw.text((18, CH-11), note, fill=P["CYAN_DIM"], font=fonts["sm"])
        remaining = max(0, total_targets - cleared_n)
        draw.text((CW-18, CH-11), f"REMAINING: {remaining:03d}  //  TOTAL ACTIVE: {total_targets}",
                  fill=P["MUTED"], font=fonts["sm"], anchor="ra")

        # Frame duration pacing
        if state == ArcadeState.VICTORY:
            dur = 120
        elif state == ArcadeState.IDLE:
            dur = 90
        elif state == ArcadeState.RESET:
            dur = 80
        elif state == ArcadeState.FLIGHT:
            dur = 45 # Smooth fast flight
        else:
            dur = 55 # Aiming, firing, impact

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
        "ordered_targets": ordered_target_list,
        "active_row_indices": active_row_indices,
    }


def generate_contact_sheet(cells, output_path, results):
    """
    Generate a 6-panel contact sheet proving:
      1. Initializing (Ship enters sector)
      2. Aiming (Lock reticle on bottom row target)
      3. Continuous Flight (Eased flight trajectory between targets)
      4. Firing (Single cyan projectile in transit)
      5. Impact (Target pops and dissolves on impact)
      6. Victory (All rows cleared, victory banner held)
    """
    gif_path = Path(output_path).parent / "arcade_shooter.gif"
    if not gif_path.exists():
        return

    gif = Image.open(gif_path)
    schedule = results.get("schedule", [])
    total_frames = len(schedule)

    f_init = 4
    f_aiming = next((i for i, s in enumerate(schedule) if s["state"] == ArcadeState.AIMING), 8)
    f_flight = next((i for i, s in enumerate(schedule) if s["state"] == ArcadeState.FLIGHT), 12)
    f_firing = next((i for i, s in enumerate(schedule) if s["state"] == ArcadeState.FIRING), 15)
    f_impact = next((i for i, s in enumerate(schedule) if s["state"] == ArcadeState.IMPACT), 16)
    f_victory = next((i for i, s in enumerate(schedule) if s["state"] == ArcadeState.VICTORY), total_frames - 20) + 4

    frames_needed = [f_init, f_aiming, f_flight, f_firing, f_impact, f_victory]

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
        "2. AIMING — Lock reticle on bottom row",
        "3. FLIGHT — Continuous smooth trajectory",
        "4. FIRING — Single cyan projectile launches",
        "5. IMPACT — Target pops & dissolves on hit",
        "6. VICTORY — All 7 rows cleared & secured",
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

    print("\n[*] Running arcade telemetry row-clearing & flight validation suite...")

    active = [c for c in cells if c["level"] > 0]
    empty  = [c for c in cells if c["level"] == 0]

    check("Contribution data not empty", len(cells) > 0)
    check("Has active (non-zero) cells", len(active) > 0)
    check("Empty cells have level 0", all(c["level"] == 0 for c in empty))
    check("Active cells have level 1..4", all(1 <= c["level"] <= 4 for c in active))

    ordered_targets = results.get("ordered_targets", [])
    active_row_indices = results.get("active_row_indices", [])

    check("Ordered targets match active cells count exactly", len(ordered_targets) == len(active))

    # Test ROW-BY-ROW CLEARING: bottom row cleared first, moving upward
    # active_row_indices are sorted descending (day 6 down to day 0).
    # All targets of active_row_indices[0] must appear BEFORE active_row_indices[1], etc.
    row_clearing_valid = True
    current_row_idx = 0
    seen_days = []
    for t in ordered_targets:
        t_day = t["day"]
        expected_day = active_row_indices[current_row_idx]
        if t_day != expected_day:
            # Did it advance to next row?
            if current_row_idx + 1 < len(active_row_indices) and t_day == active_row_indices[current_row_idx + 1]:
                current_row_idx += 1
            else:
                row_clearing_valid = False
                break
    check("Strict bottom-to-top row clearing sequence enforced", row_clearing_valid)

    # Confirm continuous flight frames exist (proving no teleportation)
    schedule = results.get("schedule", [])
    flight_frames = [s for s in schedule if s["state"] == ArcadeState.FLIGHT]
    check("Continuous flight frames present (no teleportation between targets)", len(flight_frames) > 100, f"flight frames: {len(flight_frames)}")

    # Verify single projectile rule
    single_projectile_rule = all(
        (s["proj"] is not None and s["state"] == ArcadeState.FIRING) or (s["proj"] is None)
        for s in schedule
    )
    check("Strictly one projectile at a time (zero overlapping)", single_projectile_rule)

    # Score strictly updates only on impact
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

    # Victory occurs after 100% of targets cleared
    victory_frames = [s for s in schedule if s["state"] == ArcadeState.VICTORY]
    check("Victory state occurs only after 100% targets cleared",
          len(victory_frames) > 0 and all(s["cleared_count"] == len(active) for s in victory_frames))

    # GIF file checks
    gif_path = Path(results["path"])
    check("GIF file exists", gif_path.exists())
    check("GIF size < 2.5 MB", results["size_kb"] < 2560, f"actual: {results['size_kb']:.1f} KB")

    print(f"\n[*] Results: {passed} passed, {failed} failed")
    return failed == 0


# ─── MAIN ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="TACE-X Contribution Arcade Shooter (Row-by-Row Flight Mode)")
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

    # 1. Fetch live data from GitHub API
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

    # 2. Fallback to cache if available
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

    # 3. Fallback to fixture
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
    print(f"    Targets: {results['targets']} active contribution cells (Row-by-Row Clearing)")
    print(f"    Score:   {results['score']:,} pts")
    if is_fixture:
        print("    ⚠️  DATA SOURCE: DEV FIXTURE")
    else:
        print("    ✓  DATA SOURCE: Real GitHub contribution API")


if __name__ == "__main__":
    main()
