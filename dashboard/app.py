import os
from flask import Flask, render_template, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("DASH_SECRET", "dev-secret")

from dashboard.routes import auth_bp
from dashboard.decorators import login_required

app.register_blueprint(auth_bp)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/dashboard")
@login_required
def dashboard():
    user = session.get("user")
    guilds = session.get("guilds", [])
    return render_template("dashboard.html", user=user, guilds=guilds)

@app.after_request
def security_headers(resp):
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
