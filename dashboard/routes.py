from flask import Blueprint, redirect, session

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    # Mock login (for testing)
    session["user"] = {
        "id": 1,
        "username": "TestUser"
    }
    return redirect("/dashboard")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
