
Marketra Bot – READY VERSION

=== QUICK SETUP ===

1) Create a .env file in project root:

   DISCORD_BOT_TOKEN=PUT_YOUR_BOT_TOKEN_HERE
   DISCORD_CLIENT_ID=YOUR_CLIENT_ID
   DISCORD_CLIENT_SECRET=YOUR_CLIENT_SECRET
   DISCORD_REDIRECT_URI=https://yourdomain.com/auth/callback
   DASH_SECRET=long-random-secret

2) Install dependencies:
   pip install -r requirements.txt

3) Run the bot:
   python bot.py

4) Run dashboard (optional):
   python dashboard/app.py

=== SECURITY ===
- Never upload .env to GitHub
- Rotate tokens if leaked

This package keeps ALL original commands and structure intact.
