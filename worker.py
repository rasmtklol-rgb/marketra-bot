import os
import time
import hikari
from database.db import Session, init_db
from database.models import Subscription

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is missing")

bot = hikari.GatewayBot(
    token=TOKEN,
    intents=hikari.Intents.GUILD_MESSAGES | hikari.Intents.MESSAGE_CONTENT,
)

# ====== DATABASE INIT ======
@bot.listen(hikari.StartedEvent)
async def on_started(event):
    init_db()
    print("Bot ready (Hikari)")

# ====== SUBSCRIPTION CHECK ======
def check_subscription(guild_id: int) -> bool:
    session = Session()
    sub = session.query(Subscription).filter_by(guild_id=str(guild_id)).first()
    session.close()

    if not sub:
        return False

    now = time.time()
    if now <= sub.expires_at:
        return True

    if now <= sub.grace_until:
        return True

    return False

# ====== COMMAND HANDLER ======
@bot.listen(hikari.MessageCreateEvent)
async def on_message(event):
    if not event.is_human:
        return

    content = event.content.strip()
    if not content.startswith("!"):
        return

    if not event.guild_id:
        await event.message.respond("❌ الأوامر تعمل داخل السيرفر فقط")
        return

    if not check_subscription(event.guild_id):
        await event.message.respond("⛔ هذا البوت يتطلب اشتراك نشط")
        return

    # ====== COMMANDS ======
    if content == "!ping":
        await event.message.respond("🏓 Pong!")

    elif content == "!help":
        await event.message.respond(
            "الأوامر المتاحة:\n"
            "!ping\n"
            "!help"
        )

bot.run()
