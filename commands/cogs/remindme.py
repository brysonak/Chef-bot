import re
import discord
from discord.ext import commands
from discord import app_commands
import asyncio


class Remindme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="remindme", description="Ping you with a reminder in [time]")
    @app_commands.choices(unit=[
    app_commands.Choice(name="Hours", value="h"),
    app_commands.Choice(name="Minutes", value="m"),
    app_commands.Choice(name="Seconds", value="s"),
])
    async def reminderCommand(self, interaction: discord.Interaction, reminder: str, time: int, unit: app_commands.Choice[str]):
            asyncio.create_task(self.reminderFunction(interaction, reminder, time, unit.value))
            await interaction.message.reply(f"Got it, reminding you to {reminder}, in {time} {unit.name}")

    async def reminderFunction(self, interaction, reminder, time, unit):
        if unit == "h":
            await asyncio.sleep(float(time)*3600)
        if unit == "m":
            await asyncio.sleep(float(time)*60)
        if unit == "s":
            await asyncio.sleep(float(time))
        await interaction.channel.send(f"{interaction.user.mention}, remember to {reminder}!")


async def setup(bot):
    await bot.add_cog(Remindme(bot))