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
        print(f"Honeypot triggered by {message.author} in {message.channel}")
        if message.channel.id != CHANNEL:
            return

        guild = message.guild
        member = message.author
        print(f"Attempting to ban {member.display_name} for triggering honeypot")
        try:
            await message.delete()
        except discord.HTTPException:
            print(f"Failed to delete message from {member.display_name} in honeypot channel")

        try:
            await guild.ban(member, reason="Honeypot channel trigger", delete_message_days=0)
        except discord.Forbidden:
            print(f"Failed to ban {member.display_name} for triggering honeypot. Ensure paulie has ban permissions.")
        except discord.HTTPException:
            print(f"HTTP error occurred while banning {member.display_name} for triggering honeypot")


async def setup(bot):
    await bot.add_cog(Honeypot(bot))