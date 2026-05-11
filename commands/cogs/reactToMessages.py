import discord
from discord.ext import commands
from pathlib import Path


CHANNELS = [1503503498497622297] # For now just the test channel
ASSET_PATH = Path(__file__).resolve().parents[2] / "assets" / "yes-chef.png"


class ReactToMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"Message received in {message.channel}")
        if message.author.bot:
            return

        if not message.channel.id in CHANNELS:
            return

        if not message.content.contains("yes chef"):
            return

        guild = message.guild
        member = message.author

        await message.channel.send(file=discord.File(str(ASSET_PATH), filename="yes-chef.png"))



async def setup(bot):
    await bot.add_cog(ReactToMessages(bot))