import discord
from discord.ext import commands


CHANNEL = 1503508650378137761

class Honeypot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"Message received in {message.channel}")
        if message.author.bot:
            return

        if message.channel.id != CHANNEL:
            return

        guild = message.guild
        member = message.author

        try:
            await message.delete()
        except discord.HTTPException:
            pass

        try:
            await guild.ban(member, reason="Honeypot channel trigger", delete_message_days=0)
        except (discord.Forbidden, discord.HTTPException):
            pass


async def setup(bot):
    await bot.add_cog(Honeypot(bot))