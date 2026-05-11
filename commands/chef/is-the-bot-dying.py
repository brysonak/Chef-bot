import discord
import psutil
import os
from discord.ext import commands

class IsTheBotDying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="areyouok")
    async def areyouok(self, ctx):
        latency = round(self.bot.latency * 1000)

        process = psutil.Process(os.getpid())
        mem_mb = round(process.memory_info().rss / 1024 / 1024, 2)

        try:
            cpu = round(process.cpu_percent(interval=0.1), 1)
            cpu_str = f"{cpu}%"
        except Exception:
            cpu_str = "unavailable"

        command_count = len([c for c in self.bot.walk_commands()])

        embed = discord.Embed(title="bot status", color=discord.Color.green())
        embed.add_field(name="latency", value=f"{latency}ms", inline=True)
        embed.add_field(name="memory", value=f"{mem_mb} MB", inline=True)
        embed.add_field(name="cpu", value=cpu_str, inline=True)
        embed.add_field(name="commands loaded", value=str(command_count), inline=True)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(IsTheBotDying(bot))