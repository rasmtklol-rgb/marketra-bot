from flask import Blueprint, redirect, session

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    # Placeholder for Discord OAuth redirect
    session["user"] = {"id": 0, "username": "admin"}
    return redirect("/dashboard")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
