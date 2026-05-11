import discord
from discord.ext import commands
from pathlib import Path


CHANNELS = [1503503498497622297]
ASSET_PATH = Path(__file__).resolve().parents[2] / "assets" / "yes-chef.png"


class ReactToMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id not in CHANNELS:
            return

        if "yes chef" not in message.content.lower():
            return

        await message.channel.send(file=discord.File(str(ASSET_PATH), filename="yes-chef.png"))


async def setup(bot):
    await bot.add_cog(ReactToMessages(bot))