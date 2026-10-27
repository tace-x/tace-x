# TACE-X // PHASE 4 PORTFOLIO & DEVELOPER UI SPECIFICATION
## Premium Portfolio Integration, Verified Project Selection & Profile Design

**GitHub Profile:** `tace-x` (https://github.com/tace-x)
**Deliverable Document:** Phase 4 Engineering Documentation
**Status:** Complete & Locally Verified

---

## 1. Executive Summary

Phase 4 transforms the `tace-x` GitHub profile from an initial cockpit skeleton into an integrated, tier-one developer portfolio. Adhering strictly to empirical verification, this phase eliminates speculative claims, resolves historical stack inaccuracies, introduces custom vector banner assets for top projects, and organizes projects into a distinct two-tier hierarchy backed by real test suites and source code.

---

## 2. Project Selection & 5-Factor Rubric Evaluation

All 13 public repositories of `@tace-x` were audited against the 5-factor portfolio rubric:

$$\text{Weighted Score} = 0.25(\text{Depth}) + 0.20(\text{Originality}) + 0.20(\text{Usefulness}) + 0.20(\text{Evidence}) + 0.15(\text{Presentation})$$

| Rank | Project | Language / Core Stack | Depth (25%) | Originality (20%) | Usefulness (20%) | Evidence (20%) | Presentation (15%) | Score (/5.0) | Tier Assignment |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | [**TerminalVision**](https://github.com/tace-x/TerminalVision) | Rust 2024, Ratatui, Unix PTY, Crossterm, Libc | 5.0 | 4.5 | 4.5 | 5.0 | 4.5 | **4.725** | **Tier 1 Flagship** |
| **#2** | [**CAPCAM**](https://github.com/tace-x/CAPCAM) | TypeScript, Chrome MV3, WebRTC, Offscreen Canvas | 4.5 | 5.0 | 4.5 | 5.0 | 4.0 | **4.625** | **Tier 1 Flagship** |
| **#3** | [**NOCAP (TruthLens)**](https://github.com/tace-x/NOCAP) | TypeScript, React 19, NVIDIA NIM, Gemma 4 | 4.5 | 4.5 | 4.5 | 4.5 | 4.0 | **4.425** | **Tier 1 Flagship** |
| **#4** | [**Kalvichat**](https://github.com/tace-x/Kalvichat) | React 19, Cloud Firestore, Firebase Auth, Node | 4.0 | 4.0 | 4.5 | 4.5 | 4.5 | **4.275** | **Tier 2 Production Lab** |
| **#5** | [**TypeTasks**](https://github.com/tace-x/TypeTasks) | TypeScript, React 18.3, Vite 8, Vitest | 3.5 | 4.0 | 4.5 | 4.0 | 4.0 | **3.975** | **Tier 2 Production Lab** |
| **#6** | [**Project-Alpha**](https://github.com/tace-x/Project-Alpha) | TypeScript, React 18, Express, Firebase Admin | 3.5 | 4.5 | 3.5 | 3.5 | 4.0 | **3.775** | **Tier 2 Production Lab** |

---

## 3. Verified Project Showcases

### 01 — TerminalVision (Rank 1 — Score 4.725)
- **Repository:** https://github.com/tace-x/TerminalVision
- **Domain:** Native Systems & Rust 2024
- **Banner Asset:** `assets/terminal-vision.svg` (900x370, Valid XML)
- **Architecture Highlights:** Dual-pane VFS with zero allocation on quiescent idle loops; live embedded Unix PTY (`zsh`/`bash`/`fish`) with instant focus toggling (`Ctrl+T`); Kitty, iTerm2, and Sixel graphics decoding with ASCII fallbacks.
- **Verification Evidence:** 21 integration test suites under `tests/` verifying PTY lifecycles, memory safety, and layout engines.

### 02 — CAPCAM (Rank 2 — Score 4.625)
- **Repository:** https://github.com/tace-x/CAPCAM
- **Domain:** Browser Systems & WebRTC Media Engineering
- **Banner Asset:** `assets/capcam.svg` (900x360, Valid XML)
- **Architecture Highlights:** Chrome Manifest V3 extension intercepting WebRTC `MediaStreamTrack` instances; offscreen canvas compositing pipeline running at 60 FPS without main-thread blocking; in-place `RTCRtpSender.replaceTrack()` hot-swapping.
- **Verification Evidence:** 15 test suites under `tests/` with Vitest, validating stream substitution, canvas lifecycle, and error isolation.

### 03 — NO CAP (TruthLens) (Rank 3 — Score 4.425)
- **Repository:** https://github.com/tace-x/NOCAP
- **Domain:** Rumour Intelligence & Fact Verification
- **Banner Asset:** `assets/nocap.svg` (900x360, Valid XML)
- **Architecture Highlights:** Forensic social claim analysis platform powered by NVIDIA NIM endpoints and Google Gemma 4; modular serverless API (`api/ai/`: `check.ts`, `enhance.ts`, `similarity.ts`, `synthesize.ts`); cosine clustering and entity predicate matching.
- **Verification Evidence:** Production TypeScript codebase with complete serverless endpoints and NVIDIA NIM integration.

### 04 — Kalvichat (Rank 4 — Score 4.275)
- **Repository:** https://github.com/tace-x/Kalvichat
- **Domain:** Secure Distributed Messaging & React 19
- **Banner Asset:** `assets/kalvi-chat.svg` (900x360, Valid XML — Modernized from historical orphan)
- **Architecture Highlights:** Real-time messaging platform leveraging React 19 transitions and Cloud Firestore snapshot channels; declarative security rules (`firestore.rules`) and compound query indexes (`firestore.indexes.json`).
- **Verification Evidence:** Complete automated test suite under `tests/` executed via native `node --test`.

### 05 — TypeTasks (Rank 5 — Score 3.975)
- **Repository:** https://github.com/tace-x/TypeTasks
- **Domain:** Productivity Engine & Flow Workspace
- **Banner Asset:** `assets/typetasks.svg` (900x350, Valid XML — Corrected stack labels)
- **Architecture Highlights:** Zero-latency keyboard interaction model (`⌘K` command hub, `J`/`K` vim flow, `Space` toggle); 100% operational offline with local storage state; live deployment on Vercel.
- **Live Demo:** https://typetask-nine.vercel.app (Verified HTTP 200)

### 06 — Project Alpha (Rank 6 — Score 3.775)
- **Repository:** https://github.com/tace-x/Project-Alpha
- **Domain:** AI & High-Stakes Decision Intelligence
- **Banner Asset:** `assets/project-alpha.svg` (900x360, Valid XML)
- **Architecture Highlights:** Adversarial counter-analysis pipeline: `Decision` ➔ `Analyze` ➔ `Challenge` ➔ `Simulate` ➔ `Verdict` ➔ `Monitor`; multi-agent simulation evaluating tail-risk scenarios.

---

## 4. Secondary Production Suites

A structured, accessible Markdown table documents operational production systems:

1. **Kalopsia:** Data-centre operations, service recovery tracking, payment auditing (Firestore, JavaScript, Chart.js).
2. **kalopsia-paliative:** Healthcare equipment logistics, inventory management, rental declarations (Firebase, JavaScript, HTML5).
3. **St. Annes Fee Portal:** Multi-surface student/administrator fee schedules and receipt generation (Firebase, JavaScript, SheetJS).
4. **School Voting System:** Offline digital secret-ballot election system with local storage and password-gated tally console (JavaScript, CSS3).

---

## 5. Technology Stack Verification & Discrepancy Resolution

### Historical Discrepancies Corrected
1. **TypeTasks Stack:** In earlier README drafts, TypeTasks claimed `React 19` and `Tailwind CSS`. Actual repository inspection confirms `React 18.3.1`, `Vite 8.3.4`, `Vitest`, and vanilla `styles.css`. README badges and SVG text (`assets/typetasks.svg`) were updated to reflect verified packages.
2. **Kalvichat Public Source:** Earlier `assets/kalvi-chat.svg` stated "No public repository listed". Modernized to point directly to `https://github.com/tace-x/Kalvichat`.
3. **CAPCAM & NOCAP Promotion:** Both repositories have deep engineering implementations and extensive test suites. Elevated from generic table rows to Tier-1 Flagship showcases with custom SVG banners.

---

## 6. Telemetry & Activity Auditing

| Service / Widget | Source | Update Frequency | Status | Mitigation / Failure Behavior |
|---|---|---|:---:|---|
| **Contribution Arcade Space Shooter** | Local Generator (`scripts/generate_arcade.py`) | Deterministic build / Pre-rendered | Verified (HTTP 200 local) | Zero network dependency; completely immune to external outages. |
| **GitHub Stats Card** | `github-readme-stats.vercel.app` | Dynamic (cached CDN) | Verified (HTTP 200) | Obsidian theme `#0B0F17` matching profile aesthetic. |
| **Top Languages Card** | `github-readme-stats.vercel.app` | Dynamic (cached CDN) | Verified (HTTP 200) | Bounded to public repository language distribution. |
| **GitHub Streak Stats** | `github-readme-streak-stats.herokuapp.com` | Dynamic (cached CDN) | Verified (HTTP 200) | Verified HTTP 200 with custom neon ring/fire tokens. |

---

## 7. Validation Results Summary

Ran `python3 scripts/validate_portfolio.py`:
- **16 SVG Assets:** 100% valid XML, all under 150 KB budget.
- **2 GIF Assets:** 100% valid animated frames, all under 2.5 MB budget.
- **44 Declared Anchor IDs:** 100% of internal navigation links resolve to declared targets.
- **18 Asset References:** 100% exist on disk.
- **24 External Href Links:** Tested with Python urllib; 0 failed, 24/24 HTTP 200.
