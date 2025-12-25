import os
import requests
from flask import Blueprint, redirect, request, session

auth_bp = Blueprint("auth", __name__)

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")

DISCORD_API = "https://discord.com/api"

@auth_bp.route("/login")
def login():
    return redirect(
        f"{DISCORD_API}/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify guilds"
    )

@auth_bp.route("/auth/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return redirect("/")

    # Exchange code for access token
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_res = requests.post(f"{DISCORD_API}/oauth2/token", data=data, headers=headers)
    token_json = token_res.json()

    access_token = token_json.get("access_token")
    if not access_token:
        return redirect("/")

    # Get user info
    user_res = requests.get(
        f"{DISCORD_API}/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user = user_res.json()

    session["user"] = {
        "id": user["id"],
        "username": user["username"],
        "avatar": user["avatar"]
    }

    # Get user guilds
    guilds_res = requests.get(
        f"{DISCORD_API}/users/@me/guilds",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    guilds = guilds_res.json()

    manageable_guilds = []
    for g in guilds:
        perms = int(g.get("permissions", 0))
        if g.get("owner") or (perms & 0x20):
            manageable_guilds.append({
                "id": g["id"],
                "name": g["name"],
                "icon": g["icon"]
            })

    session["guilds"] = manageable_guilds

    return redirect("/dashboard")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
