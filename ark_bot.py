import os
import discord
import requests
from discord.ext import commands
from discord.ext.commands import has_role, CheckFailure
from dotenv import load_dotenv # test

# Load secrets from .env
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
NITRADO_TOKEN = os.getenv("NITRADO_TOKEN")
SERVICE_ID = os.getenv("SERVICE_ID")

API_BASE = "https://api.nitrado.net"
HEADERS = {
    "Authorization": f"Bearer {NITRADO_TOKEN}",
    "Content-Type": "application/json"
}

# Change this to match your server's admin role name
REQUIRED_ROLE = "admin"

# Enable message content intent
intents = discord.Intents.default()
intents.message_content = True

# Set command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# ARK Server: Start (Admins only)
@bot.command(name='start_server')
@has_role(REQUIRED_ROLE)
async def start_server(ctx):
    url = f"{API_BASE}/services/{SERVICE_ID}/gameservers/restart"
    r = requests.post(url, headers=HEADERS)
    try:
        data = r.json()
        await ctx.send(f"🚀 Restart server response:\n```json\n{data}\n```")
    except Exception:
        await ctx.send(f"❌ Failed to restart/start server.\nStatus Code: {r.status_code}\nResponse: {r.text}")

# ARK Server: Stop (Admins only)
@bot.command(name='stop_server')
@has_role(REQUIRED_ROLE)
async def stop_server(ctx):
    url = f"{API_BASE}/services/{SERVICE_ID}/gameservers/stop"
    r = requests.post(url, headers=HEADERS)
    try:
        data = r.json()
        await ctx.send(f"🛑 Stop server response:\n```json\n{data}\n```")
    except Exception:
        await ctx.send(f"❌ Failed to stop server.\nStatus Code: {r.status_code}\nResponse: {r.text}")

# ARK Server: Status (Admins only)
@bot.command(name='status')
@has_role(REQUIRED_ROLE)
async def status(ctx):
    url = f"{API_BASE}/services/{SERVICE_ID}"
    r = requests.get(url, headers=HEADERS)
    try:
        status = r.json()["data"]["service"]["status"]
        await ctx.send(f"📡 Server status: `{status}`")
    except Exception:
        await ctx.send(f"❌ Failed to fetch status.\nStatus Code: {r.status_code}\nResponse: {r.text}")

# Ping command to test bot (public)
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# Optional debug command (public)
@bot.event
async def on_message(message):
    print(f"🔍 Message from {message.author}: {message.content}")

    if message.author == bot.user:
        return

    if message.content == "!debug":
        await message.channel.send("🧪 Bot is alive and reading messages.")

    await bot.process_commands(message)

# Handle permission errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("🚫 You do not have permission to use this command.")
    else:
        raise error

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
