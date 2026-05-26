import re
import discord
from discord.ext import commands

PATTERN = re.compile(r"how\s+(do\s+i|can\s+i)\s+play", re.IGNORECASE)


class How(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if PATTERN.search(message.content):
            await message.reply("You can start playing by entering [our playtest](https://nightmare-kitchen.firstlook.gg/)!")


async def setup(bot):
    await bot.add_cog(How(bot))