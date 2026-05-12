import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

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
    try:
        asyncio.run(main())
    finally:
        import sys
        sys.exit(-1) #If running with the botscript, -1 will cause the script to restart the bot. This also means if there is a truly fatal error,
        #The script will handle restarting the bot.
        #Note that python syntax errors will prevent the bot from starting.