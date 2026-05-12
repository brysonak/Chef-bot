import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv
import aiohttp

load_dotenv()

CHEF_PREFIX = "chef "
DEFAULT_PREFIX = os.getenv("DEFAULT_PREFIX", "!")

COGS_PATH = "commands.cogs"
CHEF_PATH = "commands.chef"

COGS = [
    "honeypot",
    "reload_changed_extension",
]

CHEF_COGS = [
    "is-the-bot-dying",
    "reactToMessages"
]


def get_prefix(bot, message):
    content = message.content.lower()
    if content.startswith(CHEF_PREFIX):
        return CHEF_PREFIX
    return DEFAULT_PREFIX


bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.tree.sync()
    if bot.user:
        print(f"logged in successfully")
    await update_status_loop.start()

async def update_status():
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=3471110"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                channel = bot.get_channel(1503503498497622297)
                
                player_count = data.get("response", 0)
                if channel:
                    await channel.send(player_count)
                player_count = player_count["player_count"] if isinstance(player_count, dict) else -1
                if channel:
                    await channel.send(player_count)
            else:
                player_count = -1
    if player_count == 1:
        await bot.change_presence(activity=discord.Game(name=f"{player_count} person playing Nightmare Kitchen on Steam!"))
    elif player_count > 1:
        await bot.change_presence(activity=discord.Game(name=f"{player_count} people playing Nightmare Kitchen on Steam!"))
    elif player_count < 0:
        await bot.change_presence(activity=discord.Game(name="Go play Nightmare Kitchen on Steam!"))
    else:
        await bot.change_presence(activity=discord.Game(name="Serving up some tasty dungeons in Nightmare Kitchen!"))

@tasks.loop(minutes=10)
async def update_status_loop():
    await update_status()

@bot.command(name="update_status")
@commands.has_permissions(manage_messages=True)
async def update_status_command(ctx):
    await update_status()
    await ctx.send("Status updated!")

async def load_cogs():
    for cog in COGS:
        await bot.load_extension(f"{COGS_PATH}.{cog}")
        print(f"loaded cog: {cog}")

    for cog in CHEF_COGS:
        await bot.load_extension(f"{CHEF_PATH}.{cog}")
        print(f"loaded chef cog: {cog}")


async def main():
    async with bot:
        await load_cogs()                   # Don't touch this comment. Even though the env exists, I still get errors. Had to remove it somehow
        await bot.start(os.getenv("TOKEN")) # pyright: ignore[reportArgumentType]


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())