from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>тожить</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, 'Segoe UI', system-ui, sans-serif;
            background: #0a0a0a;
            color: #edecec;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* --- Phase 1: Input screen --- */
        #phase1 {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 2;
        }
        .card {
            width: 100%;
            max-width: 460px;
            padding: 48px 40px;
            text-align: center;
        }
        .label {
            font-size: 1.05rem;
            color: rgba(237, 236, 236, 0.55);
            margin-bottom: 24px;
        }
        .input-wrap {
            position: relative;
            margin-bottom: 20px;
        }
        .card input {
            width: 100%;
            padding: 14px 20px;
            background: rgba(237, 236, 236, 0.06);
            border: 1px solid rgba(237, 236, 236, 0.1);
            border-radius: 10px;
            color: #edecec;
            font-size: 1.1rem;
            font-family: inherit;
            text-align: center;
            outline: none;
            transition: border-color 0.2s;
        }
        .card input:focus { border-color: rgba(237, 236, 236, 0.25); }
        .card input.error {
            border-color: #e94560;
            animation: shake 0.4s;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-6px); }
            75% { transform: translateX(6px); }
        }
        .btn {
            width: 100%;
            padding: 14px 20px;
            background: rgba(237, 236, 236, 0.08);
            border: 1px solid rgba(237, 236, 236, 0.1);
            border-radius: 10px;
            color: #edecec;
            font-size: 1rem;
            font-family: inherit;
            cursor: pointer;
            transition: background 0.2s, border-color 0.2s;
        }
        .btn:hover {
            background: rgba(237, 236, 236, 0.12);
            border-color: rgba(237, 236, 236, 0.2);
        }
        .result {
            margin-top: 32px;
            opacity: 0;
            transform: translateY(10px);
            transition: opacity 0.5s, transform 0.5s;
        }
        .result.visible { opacity: 1; transform: translateY(0); }
        .result .equals {
            font-size: 2.4rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            margin-bottom: 8px;
        }
        .result .explanation {
            color: rgba(237, 236, 236, 0.55);
            font-size: 0.95rem;
            line-height: 1.6;
        }
        .hint {
            margin-top: 8px;
            font-size: 0.85rem;
            color: #e94560;
            min-height: 22px;
        }

        /* --- "Want more" button --- */
        .want-more {
            margin-top: 28px;
            opacity: 0;
            transform: translateY(10px);
            transition: opacity 0.6s 0.4s, transform 0.6s 0.4s;
        }
        .want-more.visible { opacity: 1; transform: translateY(0); }
        .want-more .btn {
            background: rgba(237, 236, 236, 0.04);
            border: 1px dashed rgba(237, 236, 236, 0.2);
            font-size: 0.95rem;
            letter-spacing: 0.02em;
        }
        .want-more .btn:hover {
            background: rgba(237, 236, 236, 0.1);
            border-style: solid;
        }

        /* --- Transition overlay --- */
        #transition {
            position: fixed;
            inset: 0;
            z-index: 100;
            pointer-events: none;
            opacity: 0;
        }
        #transition canvas {
            width: 100%;
            height: 100%;
        }

        /* --- Phase 2: Final message --- */
        #phase2 {
            min-height: 100vh;
            display: none;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.8s;
        }
        #phase2.visible { opacity: 1; }
        #phase2 .final-text {
            font-size: 4rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            text-align: center;
        }

        /* --- Stars for transition --- */
        .star {
            position: fixed;
            width: 2px; height: 2px;
            background: #edecec;
            border-radius: 50%;
            z-index: 101;
            pointer-events: none;
        }
    </style>
</head>
<body>

<!-- Phase 1 -->
<div id="phase1">
    <div class="card">
        <div class="label">Введи слово «тожить»</div>
        <div class="input-wrap">
            <input type="text" id="word" placeholder="тожить" autocomplete="off" autofocus />
            <div class="hint" id="hint"></div>
        </div>
        <button class="btn" onclick="check()">Проверить значение слова «тожить»</button>
        <div class="result" id="result">
            <div class="equals">тожить = тоже</div>
            <div class="explanation">«тожить» — это «тоже».<br>Тож + ить = тож + е.<br>Один корень — одно значение.</div>
        </div>
        <div class="want-more" id="wantMore">
            <button class="btn" onclick="startTransition()">Хочу знать больше</button>
        </div>
    </div>
</div>

<!-- Transition overlay -->
<div id="transition">
    <canvas id="warpCanvas"></canvas>
</div>

<!-- Phase 2: Final -->
<div id="phase2">
    <div class="final-text">ты пидор</div>
</div>

<script>
    // --- Phase 1 logic ---
    const wordInput = document.getElementById('word');
    const hintEl = document.getElementById('hint');
    const resultEl = document.getElementById('result');
    const wantMoreEl = document.getElementById('wantMore');

    wordInput.addEventListener('keydown', e => { if (e.key === 'Enter') check(); });
    wordInput.addEventListener('input', () => {
        wordInput.classList.remove('error');
        hintEl.textContent = '';
        resultEl.classList.remove('visible');
        wantMoreEl.classList.remove('visible');
    });

    function check() {
        const val = wordInput.value.trim().toLowerCase();
        if (val === 'тожить') {
            wordInput.classList.remove('error');
            hintEl.textContent = '';
            resultEl.classList.add('visible');
            wantMoreEl.classList.add('visible');
        } else {
            wordInput.classList.add('error');
            resultEl.classList.remove('visible');
            wantMoreEl.classList.remove('visible');
            hintEl.textContent = val ? 'Это не «тожить». Попробуй ещё раз.' : 'Введи слово «тожить»';
            setTimeout(() => wordInput.classList.remove('error'), 400);
        }
    }

    // --- Warp transition ---
    function startTransition() {
        const overlay = document.getElementById('transition');
        const canvas = document.getElementById('warpCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        overlay.style.opacity = '1';
        overlay.style.pointerEvents = 'all';

        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        const stars = [];
        for (let i = 0; i < 400; i++) {
            const angle = Math.random() * Math.PI * 2;
            const dist = Math.random() * 50 + 10;
            stars.push({
                x: cx + Math.cos(angle) * dist,
                y: cy + Math.sin(angle) * dist,
                angle: angle,
                speed: Math.random() * 2 + 1,
                dist: dist,
                len: 1,
                alpha: Math.random() * 0.5 + 0.5
            });
        }

        let frame = 0;
        const totalFrames = 120;

        function animate() {
            frame++;
            const progress = frame / totalFrames;
            const accel = 1 + progress * 40;

            ctx.fillStyle = `rgba(10, 10, 10, ${0.15 + progress * 0.1})`;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            for (const s of stars) {
                s.dist += s.speed * accel;
                s.len = Math.min(s.speed * accel * 1.5, 120);
                const x = cx + Math.cos(s.angle) * s.dist;
                const y = cy + Math.sin(s.angle) * s.dist;
                const x2 = cx + Math.cos(s.angle) * (s.dist - s.len);
                const y2 = cy + Math.sin(s.angle) * (s.dist - s.len);

                const grad = ctx.createLinearGradient(x2, y2, x, y);
                grad.addColorStop(0, `rgba(237, 236, 236, 0)`);
                grad.addColorStop(1, `rgba(237, 236, 236, ${s.alpha})`);

                ctx.beginPath();
                ctx.moveTo(x2, y2);
                ctx.lineTo(x, y);
                ctx.strokeStyle = grad;
                ctx.lineWidth = 1.5 + progress;
                ctx.stroke();
            }

            // Flash at the end
            if (progress > 0.85) {
                const flashAlpha = (progress - 0.85) / 0.15;
                ctx.fillStyle = `rgba(237, 236, 236, ${flashAlpha})`;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            if (frame < totalFrames) {
                requestAnimationFrame(animate);
            } else {
                // White flash then fade to phase 2
                ctx.fillStyle = '#edecec';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                setTimeout(() => {
                    document.getElementById('phase1').style.display = 'none';
                    document.getElementById('phase2').style.display = 'flex';

                    // Fade overlay out, reveal chat
                    let fadeFrame = 0;
                    const fadeDuration = 60;
                    function fadeOut() {
                        fadeFrame++;
                        const p = fadeFrame / fadeDuration;
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.fillStyle = `rgba(237, 236, 236, ${1 - p})`;
                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                        if (fadeFrame < fadeDuration) {
                            requestAnimationFrame(fadeOut);
                        } else {
                            overlay.style.opacity = '0';
                            overlay.style.pointerEvents = 'none';
                        }
                    }
                    fadeOut();
                    setTimeout(() => document.getElementById('phase2').classList.add('visible'), 100);
                }, 300);
            }
        }
        // Initial black
        ctx.fillStyle = '#0a0a0a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        animate();
    }

</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
