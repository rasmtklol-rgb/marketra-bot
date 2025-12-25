import os
from flask import Flask,session,redirect,render_template
from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)
app.secret_key=os.getenv("FLASK_SECRET_KEY")

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)


from dashboard.auth.routes import auth_bp
from dashboard.auth.decorators import login_required

app.register_blueprint(auth_bp)

@app.after_request
def security_headers(resp):
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp
