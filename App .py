from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>BetPawa Match Analyzer</title>
    <style>
        body {font-family: Arial; background: #101827; color: white;
              padding: 20px; max-width: 600px; margin: auto;}
        input, select, button {padding: 12px; margin: 6px 0;
              width: 100%; box-sizing: border-box; border-radius: 8px;}
        button {background: #16a34a; color: white; border: 0; font-weight: bold;}
        .card {background: #1e293b; padding: 15px; border-radius: 10px;}
    </style>
</head>
<body>
<h2>⚽ BetPawa Match Analyzer</h2>
<div class="card">
<form method="post">
<label>Home team</label>
<input name="home" required placeholder="e.g. Arsenal">
<label>Away team</label>
<input name="away" required placeholder="e.g. Chelsea">
<label>Home win probability (%)</label>
<input name="hp" type="number" min="0" max="100" required>
<label>Draw probability (%)</label>
<input name="dp" type="number" min="0" max="100" required>
<label>Away win probability (%)</label>
<input name="ap" type="number" min="0" max="100" required>
<button type="submit">Analyze match</button>
</form>
{% if result %}
<h3>{{ result }}</h3>
<p>{{ detail }}</p>
{% endif %}
</div>
<p>Estimates are not guarantees. Verify match statistics before betting.</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = detail = None
    if os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
        pass
    if __import__("flask").request.method == "POST":
        from flask import request
        home_team = request.form["home"]
        away_team = request.form["away"]
        hp = float(request.form["hp"])
        dp = float(request.form["dp"])
        ap = float(request.form["ap"])
        if abs(hp + dp + ap - 100) > 1:
            result = "Check your probabilities"
            detail = "Home, draw and away probabilities should total 100%."
        else:
            result = max(
                [(hp, "Home win"), (dp, "Draw"), (ap, "Away win")]
            )[1]
            detail = f"{home_team} vs {away_team}. Highest entered probability: {max(hp, dp, ap):.1f}%. This is your input, not an independently verified prediction."
    return render_template_string(HTML, result=result, detail=detail)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
