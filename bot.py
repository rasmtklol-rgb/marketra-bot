
import os,time,asyncio,discord
from discord.ext import commands
from dotenv import load_dotenv
from database.db import init_db
from database.models import Subscription
from database.db import Session

load_dotenv()
TOKEN=os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is missing")
    
intents=discord.Intents.default()
intents.message_content=True
bot=commands.Bot(command_prefix="!",intents=intents)

@bot.check
async def sub_guard(ctx):
    if not ctx.guild: return True
    s=Session()
    sub=s.query(Subscription).filter_by(guild_id=ctx.guild.id).first()
    s.close()
    if not sub: 
        await ctx.send("⛔ البوت يتطلب اشتراك")
        return False
    now=time.time()
    if now<=sub.expires_at: return True
    if now<=sub.grace_until:
        await ctx.send("⚠️ الاشتراك منتهي – مهلة 48 ساعة")
        return True
    await ctx.send("⛔ تم إيقاف البوت لانتهاء الاشتراك")
    return False

@bot.event
async def on_ready():
    init_db()
    print("Bot ready")

async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
