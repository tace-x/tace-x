/**
 * TACE-X // CONTRIBUTION SPACE DEFENDER
 * Pure HTML5 Canvas 60 FPS Retro Space Shooter
 * Zero external libraries, zero dependencies, built-in Web Audio synthesis.
 */

(function () {
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");

  // Game dimensions
  const WIDTH = 840;
  const HEIGHT = 480;

  // Sound Engine (Web Audio API)
  let audioCtx = null;
  let soundEnabled = true;

  function initAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        audioCtx = new AudioContext();
      }
    }
    if (audioCtx && audioCtx.state === "suspended") {
      audioCtx.resume();
    }
  }

  function playSound(type) {
    if (!soundEnabled || !audioCtx) return;
    try {
      const now = audioCtx.currentTime;
      if (type === "laser") {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(880, now);
        osc.frequency.exponentialRampToValueAtTime(180, now + 0.08);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.08);
      } else if (type === "hit") {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "square";
        osc.frequency.setValueAtTime(440, now);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.05);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.05);
      } else if (type === "explosion") {
        // Noise buffer synthesis
        const bufferSize = audioCtx.sampleRate * 0.25;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          data[i] = Math.random() * 2 - 1;
        }
        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        const filter = audioCtx.createBiquadFilter();
        filter.type = "lowpass";
        filter.frequency.setValueAtTime(600, now);
        filter.frequency.linearRampToValueAtTime(50, now + 0.25);
        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
        noise.connect(filter);
        filter.connect(gain);
        gain.connect(audioCtx.destination);
        noise.start(now);
        noise.stop(now + 0.25);
      }
    } catch (e) {
      // Audio fallback silent
    }
  }

  // Colors
  const COLORS = {
    VOID: "#0B0F17",
    DARK_CYANITE: "#070A0F",
    SHADOW: "#111C2D",
    MID_SHADOW: "#1E293B",
    CYAN: "#00F0FF",
    MINT: "#10B981",
    VIOLET: "#8B5CF6",
    RED: "#F43F5E",
    AMBER: "#F59E0B",
    WHITE: "#F8FAFC",
    MUTED: "#94A3B8",
  };

  const INVADER_COLORS = {
    0: COLORS.SHADOW,
    1: COLORS.MINT,
    2: COLORS.CYAN,
    3: COLORS.VIOLET,
    4: COLORS.RED,
  };

  // Game State
  let state = "PLAYING"; // PLAYING, PAUSED, GAMEOVER, VICTORY
  let score = 4070; // Baseline verified score
  let highScore = parseInt(localStorage.getItem("tacex_arcade_hi") || "4255", 10);
  let lives = 3;
  let wave = 1;
  let tick = 0;

  // Starfield
  const stars = [];
  for (let i = 0; i < 70; i++) {
    stars.push({
      x: Math.random() * WIDTH,
      y: Math.random() * HEIGHT,
      size: Math.random() > 0.8 ? 2 : 1,
      speed: 0.2 + Math.random() * 0.8,
      color: Math.random() > 0.6 ? COLORS.CYAN : COLORS.MID_SHADOW,
    });
  }

  // Player Ship
  const player = {
    x: WIDTH / 2,
    y: 430,
    w: 28,
    h: 20,
    speed: 6,
    cooldown: 0,
    maxCooldown: 12,
  };

  // Lasers & Enemy Projectiles
  let playerLasers = [];
  let enemyBombs = [];
  let particles = [];

  // Invaders (53 cols x 7 rows)
  const COLS = 53;
  const ROWS = 7;
  const CELL_SIZE = 11;
  const CELL_GAP = 4;
  let fleetX = 24;
  let fleetY = 60;
  let fleetDir = 1;
  let fleetSpeed = 0.4;
  let fleetDropTimer = 0;
  let invaders = [];

  function initFleet() {
    invaders = [];
    // Verified contribution pattern distribution
    for (let c = 0; c < COLS; c++) {
      for (let r = 0; r < ROWS; r++) {
        // Deterministic pseudo level
        let lvl = 0;
        const hash = (c * 17 + r * 31 + c * r) % 100;
        if (hash > 96) lvl = 4;
        else if (hash > 90) lvl = 3;
        else if (hash > 78) lvl = 2;
        else if (hash > 58) lvl = 1;

        if (lvl > 0 || Math.random() > 0.3) {
          invaders.push({
            c,
            r,
            level: lvl,
            hp: lvl === 4 ? 4 : (lvl === 3 ? 3 : (lvl === 2 ? 2 : 1)),
            alive: true,
          });
        }
      }
    }
  }

  initFleet();

  // Input Handling
  const keys = {};
  window.addEventListener("keydown", (e) => {
    initAudio();
    keys[e.code] = true;
    if (e.code === "KeyP") {
      state = state === "PLAYING" ? "PAUSED" : "PLAYING";
    }
    if (e.code === "KeyR" && (state === "GAMEOVER" || state === "VICTORY")) {
      restartGame();
    }
    if (e.code === "KeyM") {
      soundEnabled = !soundEnabled;
    }
  });

  window.addEventListener("keyup", (e) => {
    keys[e.code] = false;
  });

  // Touch button support
  const btnLeft = document.getElementById("btnLeft");
  const btnRight = document.getElementById("btnRight");
  const btnShoot = document.getElementById("btnShoot");

  if (btnLeft && btnRight && btnShoot) {
    const bindTouch = (btn, code) => {
      btn.addEventListener("touchstart", (e) => {
        e.preventDefault();
        initAudio();
        keys[code] = true;
      });
      btn.addEventListener("touchend", (e) => {
        e.preventDefault();
        keys[code] = false;
      });
    };
    bindTouch(btnLeft, "ArrowLeft");
    bindTouch(btnRight, "ArrowRight");
    bindTouch(btnShoot, "Space");
  }

  function restartGame() {
    score = 4070;
    lives = 3;
    wave = 1;
    player.x = WIDTH / 2;
    playerLasers = [];
    enemyBombs = [];
    particles = [];
    fleetX = 24;
    fleetY = 60;
    fleetDir = 1;
    initFleet();
    state = "PLAYING";
  }

  function spawnExplosion(x, y, color, count = 16) {
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const spd = 1.5 + Math.random() * 4.5;
      particles.push({
        x,
        y,
        vx: Math.cos(angle) * spd,
        vy: Math.sin(angle) * spd,
        life: 1.0,
        decay: 0.02 + Math.random() * 0.03,
        color: Math.random() > 0.5 ? color : COLORS.WHITE,
        size: Math.random() > 0.6 ? 3 : 2,
      });
    }
  }

  // Main Update Loop
  function update() {
    tick++;

    if (state !== "PLAYING") return;

    // Starfield animation
    for (const s of stars) {
      s.y += s.speed;
      if (s.y > HEIGHT) {
        s.y = 0;
        s.x = Math.random() * WIDTH;
      }
    }

    // Player Movement
    if (keys["ArrowLeft"] || keys["KeyA"]) {
      player.x -= player.speed;
    }
    if (keys["ArrowRight"] || keys["KeyD"]) {
      player.x += player.speed;
    }
    player.x = Math.max(20, Math.min(WIDTH - 20, player.x));

    // Player Shooting
    if (player.cooldown > 0) player.cooldown--;
    if ((keys["Space"] || keys["ArrowUp"] || keys["KeyW"]) && player.cooldown <= 0) {
      playerLasers.push({ x: player.x - 10, y: player.y - 10, vy: -9 });
      playerLasers.push({ x: player.x + 10, y: player.y - 10, vy: -9 });
      player.cooldown = player.maxCooldown;
      playSound("laser");
    }

    // Update Player Lasers
    for (let i = playerLasers.length - 1; i >= 0; i--) {
      const l = playerLasers[i];
      l.y += l.vy;
      if (l.y < 50) {
        playerLasers.splice(i, 1);
        continue;
      }

      // Check collision with invaders
      for (const inv of invaders) {
        if (!inv.alive) continue;
        const ix = fleetX + inv.c * (CELL_SIZE + CELL_GAP);
        const iy = fleetY + inv.r * (CELL_SIZE + CELL_GAP);

        if (l.x >= ix && l.x <= ix + CELL_SIZE && l.y >= iy && l.y <= iy + CELL_SIZE) {
          playerLasers.splice(i, 1);
          inv.hp--;
          playSound("hit");
          if (inv.hp <= 0) {
            inv.alive = false;
            const pts = (inv.level + 1) * 25;
            score += pts;
            if (score > highScore) {
              highScore = score;
              localStorage.setItem("tacex_arcade_hi", highScore);
            }
            spawnExplosion(ix + CELL_SIZE / 2, iy + CELL_SIZE / 2, INVADER_COLORS[inv.level], 16);
            playSound("explosion");
          } else {
            spawnExplosion(ix + CELL_SIZE / 2, iy + CELL_SIZE / 2, COLORS.WHITE, 4);
          }
          break;
        }
      }
    }

    // Move Fleet
    let minX = WIDTH;
    let maxX = 0;
    let aliveCount = 0;
    for (const inv of invaders) {
      if (!inv.alive) continue;
      aliveCount++;
      const ix = fleetX + inv.c * (CELL_SIZE + CELL_GAP);
      if (ix < minX) minX = ix;
      if (ix + CELL_SIZE > maxX) maxX = ix + CELL_SIZE;
    }

    if (aliveCount === 0) {
      state = "VICTORY";
      return;
    }

    fleetX += fleetDir * fleetSpeed;
    if (maxX >= WIDTH - 16) {
      fleetDir = -1;
      fleetY += 4;
    } else if (minX <= 16) {
      fleetDir = 1;
      fleetY += 4;
    }

    // Enemy Bomb Drops
    if (Math.random() < 0.035 && invaders.length > 0) {
      const livingInvaders = invaders.filter((inv) => inv.alive);
      if (livingInvaders.length > 0) {
        const shooter = livingInvaders[Math.floor(Math.random() * livingInvaders.length)];
        const bx = fleetX + shooter.c * (CELL_SIZE + CELL_GAP) + CELL_SIZE / 2;
        const by = fleetY + shooter.r * (CELL_SIZE + CELL_GAP) + CELL_SIZE;
        enemyBombs.push({ x: bx, y: by, vy: 3.5 });
      }
    }

    // Update Enemy Bombs
    for (let i = enemyBombs.length - 1; i >= 0; i--) {
      const b = enemyBombs[i];
      b.y += b.vy;
      if (b.y > HEIGHT) {
        enemyBombs.splice(i, 1);
        continue;
      }

      // Check collision with player
      if (Math.abs(b.x - player.x) < player.w / 2 && Math.abs(b.y - player.y) < player.h / 2) {
        enemyBombs.splice(i, 1);
        lives--;
        spawnExplosion(player.x, player.y, COLORS.RED, 24);
        playSound("explosion");
        if (lives <= 0) {
          state = "GAMEOVER";
        }
      }
    }

    // Update Particles
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.life -= p.decay;
      if (p.life <= 0) {
        particles.splice(i, 1);
      }
    }
  }

  // Main Render Loop
  function render() {
    ctx.fillStyle = COLORS.VOID;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // 1. Stars
    for (const s of stars) {
      ctx.fillStyle = s.color;
      ctx.fillRect(s.x, s.y, s.size, s.size);
    }

    // 2. Top HUD Bar
    ctx.fillStyle = COLORS.DARK_CYANITE;
    ctx.fillRect(0, 0, WIDTH, 48);
    ctx.strokeStyle = COLORS.CYAN;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(0, 48);
    ctx.lineTo(WIDTH, 48);
    ctx.stroke();

    ctx.font = "bold 13px 'JetBrains Mono', Courier, monospace";
    ctx.fillStyle = COLORS.MINT;
    ctx.fillText("TACE-X // DEFENDER", 20, 28);

    ctx.fillStyle = COLORS.CYAN;
    ctx.fillText(`SCORE: ${String(score).padStart(6, "0")}`, 280, 28);

    ctx.fillStyle = COLORS.VIOLET;
    ctx.fillText(`HI: ${String(highScore).padStart(6, "0")}`, 460, 28);

    ctx.fillStyle = COLORS.RED;
    ctx.fillText(`LIVES: ${"❤ ".repeat(Math.max(0, lives))}`, 620, 28);

    ctx.fillStyle = soundEnabled ? COLORS.MINT : COLORS.MUTED;
    ctx.fillText(soundEnabled ? "SND: ON" : "SND: OFF", 740, 28);

    // 3. Invader Fleet
    for (const inv of invaders) {
      if (!inv.alive) continue;
      const ix = fleetX + inv.c * (CELL_SIZE + CELL_GAP);
      const iy = fleetY + inv.r * (CELL_SIZE + CELL_GAP);

      ctx.fillStyle = INVADER_COLORS[inv.level];
      ctx.fillRect(ix, iy, CELL_SIZE, CELL_SIZE);
      ctx.strokeStyle = COLORS.MID_SHADOW;
      ctx.strokeRect(ix, iy, CELL_SIZE, CELL_SIZE);

      if (inv.level > 0) {
        ctx.fillStyle = COLORS.WHITE;
        ctx.fillRect(ix + 3, iy + 3, CELL_SIZE - 6, CELL_SIZE - 6);
      }
    }

    // 4. Lasers & Bombs
    ctx.fillStyle = COLORS.CYAN;
    for (const l of playerLasers) {
      ctx.fillRect(l.x - 1, l.y - 6, 3, 10);
      ctx.fillStyle = COLORS.WHITE;
      ctx.fillRect(l.x, l.y - 4, 1, 6);
      ctx.fillStyle = COLORS.CYAN;
    }

    ctx.fillStyle = COLORS.RED;
    for (const b of enemyBombs) {
      ctx.fillRect(b.x - 2, b.y - 4, 4, 8);
      ctx.fillStyle = COLORS.WHITE;
      ctx.fillRect(b.x - 1, b.y - 2, 2, 4);
      ctx.fillStyle = COLORS.RED;
    }

    // 5. Particles
    for (const p of particles) {
      ctx.fillStyle = p.color;
      ctx.globalAlpha = p.life;
      ctx.fillRect(p.x - p.size / 2, p.y - p.size / 2, p.size, p.size);
      ctx.globalAlpha = 1.0;
    }

    // 6. Player Ship
    if (lives > 0) {
      ctx.save();
      ctx.translate(player.x, player.y);
      // Wing lasers
      ctx.fillStyle = COLORS.CYAN;
      ctx.fillRect(-12, -6, 2, 8);
      ctx.fillRect(10, -6, 2, 8);
      // Main Hull
      ctx.fillStyle = COLORS.MID_SHADOW;
      ctx.beginPath();
      ctx.moveTo(0, -14);
      ctx.lineTo(14, 6);
      ctx.lineTo(0, 2);
      ctx.lineTo(-14, 6);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = COLORS.CYAN;
      ctx.stroke();

      // Cockpit
      ctx.fillStyle = COLORS.WHITE;
      ctx.beginPath();
      ctx.arc(0, -3, 3, 0, Math.PI * 2);
      ctx.fill();

      // Engine flames
      const flame = 3 + (tick % 4);
      ctx.fillStyle = tick % 2 === 0 ? COLORS.MINT : COLORS.CYAN;
      ctx.fillRect(-5, 6, 3, flame);
      ctx.fillRect(2, 6, 3, flame);
      ctx.restore();
    }

    // 7. Overlay Screens
    if (state === "PAUSED") {
      ctx.fillStyle = "rgba(11, 15, 23, 0.75)";
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = COLORS.CYAN;
      ctx.font = "bold 24px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText("PAUSED", WIDTH / 2, HEIGHT / 2);
      ctx.font = "14px 'JetBrains Mono', monospace";
      ctx.fillStyle = COLORS.MUTED;
      ctx.fillText("Press P to resume", WIDTH / 2, HEIGHT / 2 + 30);
      ctx.textAlign = "left";
    } else if (state === "GAMEOVER") {
      ctx.fillStyle = "rgba(11, 15, 23, 0.85)";
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = COLORS.RED;
      ctx.font = "bold 28px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText("DEFENSE FAILED", WIDTH / 2, HEIGHT / 2 - 20);
      ctx.font = "16px 'JetBrains Mono', monospace";
      ctx.fillStyle = COLORS.CYAN;
      ctx.fillText(`FINAL SCORE: ${score} PTS`, WIDTH / 2, HEIGHT / 2 + 15);
      ctx.fillStyle = COLORS.MINT;
      ctx.fillText("PRESS R TO RE-ENGAGE FLEET", WIDTH / 2, HEIGHT / 2 + 50);
      ctx.textAlign = "left";
    } else if (state === "VICTORY") {
      ctx.fillStyle = "rgba(11, 15, 23, 0.85)";
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = COLORS.MINT;
      ctx.font = "bold 28px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText("CONTRIBUTION FLEET CLEARED!", WIDTH / 2, HEIGHT / 2 - 20);
      ctx.font = "16px 'JetBrains Mono', monospace";
      ctx.fillStyle = COLORS.CYAN;
      ctx.fillText(`BONUS SCORE: ${score} PTS`, WIDTH / 2, HEIGHT / 2 + 15);
      ctx.fillStyle = COLORS.WHITE;
      ctx.fillText("PRESS R TO REPLAY WAVE", WIDTH / 2, HEIGHT / 2 + 50);
      ctx.textAlign = "left";
    }
  }

  function loop() {
    update();
    render();
    requestAnimationFrame(loop);
  }

  requestAnimationFrame(loop);
})();
