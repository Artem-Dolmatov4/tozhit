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
            display: flex;
            align-items: center;
            justify-content: center;
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
        input {
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
        input:focus {
            border-color: rgba(237, 236, 236, 0.25);
        }
        input.error {
            border-color: #e94560;
            animation: shake 0.4s;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-6px); }
            75% { transform: translateX(6px); }
        }
        button {
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
        button:hover {
            background: rgba(237, 236, 236, 0.12);
            border-color: rgba(237, 236, 236, 0.2);
        }
        .result {
            margin-top: 32px;
            opacity: 0;
            transform: translateY(10px);
            transition: opacity 0.5s, transform 0.5s;
        }
        .result.visible {
            opacity: 1;
            transform: translateY(0);
        }
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
    </style>
</head>
<body>
    <div class="card">
        <div class="label">Введи слово «тожить»</div>
        <div class="input-wrap">
            <input type="text" id="word" placeholder="тожить" autocomplete="off" autofocus />
            <div class="hint" id="hint"></div>
        </div>
        <button onclick="check()">Проверить значение слова «тожить»</button>
        <div class="result" id="result">
            <div class="equals">тожить = тоже</div>
            <div class="explanation">«тожить» — это «тоже».<br>Тож + ить = тож + е.<br>Один корень — одно значение.</div>
        </div>
    </div>
    <script>
        const input = document.getElementById('word');
        const hint = document.getElementById('hint');
        const result = document.getElementById('result');

        input.addEventListener('keydown', e => {
            if (e.key === 'Enter') check();
        });

        input.addEventListener('input', () => {
            input.classList.remove('error');
            hint.textContent = '';
            result.classList.remove('visible');
        });

        function check() {
            const val = input.value.trim().toLowerCase();
            if (val === 'тожить') {
                input.classList.remove('error');
                hint.textContent = '';
                result.classList.add('visible');
            } else {
                input.classList.add('error');
                result.classList.remove('visible');
                if (!val) {
                    hint.textContent = 'Введи слово «тожить»';
                } else {
                    hint.textContent = 'Это не «тожить». Попробуй ещё раз.';
                }
                setTimeout(() => input.classList.remove('error'), 400);
            }
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
