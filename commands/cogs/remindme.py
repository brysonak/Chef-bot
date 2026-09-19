import re
import discord
from discord.ext import commands
import asyncio


class Remindme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.lower() == "!remindme":
            await message.reply(f'Usage: !remindme |<what to be reminded of>|<time to wait>|<unit (S, M, H)>".\nNote: the |{"'"}s are necessary, as without them I can{"'"}t understand your message')
            return

        if message.content.lower().startswith("!remindme "):
            contents = message.content.split("|")
            if len(contents) < 4 or len(contents[2]) < 1 or len(contents[3]) < 1:
                await message.reply(f'Usage: !remindme "<what to be reminded of>" "<time to wait> <unit (S, M, H)>".\nNote: the quotations are necessary, as without them I can{"'"}t understand your message')
                return
            reminder = contents[1]
            time = contents[2]
            unit = contents[3]
            asyncio.create_task(self.reminderFunction(message, reminder, time, unit))
            await message.reply(f"Got it, reminding you to {reminder}, in {time}{unit}")

    async def reminderFunction(self, message, reminder, time, unit):
        unit = unit.srtip().lower()[0:1]
        if unit == "h":
            await asyncio.sleep(float(time)*3600)
        if unit == "m":
            await asyncio.sleep(float(time)*60)
        if unit == "s":
            await asyncio.sleep(float(time))
        await message.channel.send(f"{message.author.mention}, remember to {reminder}!")


async def setup(bot):
    await bot.add_cog(Remindme(bot))