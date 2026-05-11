import discord
import psutil
import os
from discord.ext import commands

class ReloadChangedExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload_extension")
    async def reload_extension(self, ctx, extension: str):
        if not "Mod Chef" in [role.name for role in ctx.author.roles] and ctx.author.id != 1354212788888932382:
            await ctx.send("You don't have permission to use this command.")
        try:
            await self.bot.reload_extension(extension)
            await ctx.send(f"Extension '{extension}' reloaded successfully.")
        except Exception as e:
            await ctx.send(f"Failed to reload extension '{extension}': {e}")



async def setup(bot):
    await bot.add_cog(ReloadChangedExtension(bot))