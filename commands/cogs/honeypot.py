# This file now just serves as general security for the server.

import discord
from discord.ext import commands
import time
import re
from datetime import timedelta

CHANNEL = 1503508650378137761
# Scam bots love to send server invites, stop em in their tracks.
DISCORD_LINK = re.compile(r"discord\.(gg|com/invite)/\S+", re.IGNORECASE)

image_tracker = {}

class Honeypot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id == CHANNEL:
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
            return

        if DISCORD_LINK.search(message.content):
            try:
                await message.delete()
            except discord.HTTPException:
                pass
            return

        image_count = sum(
            1 for a in message.attachments
            if a.content_type and a.content_type.startswith("image/")
        )
        # If the user sends 4 images or more within a 5 second window, delete it and time them out
        # Scam bots are most prevalent with this
        if image_count > 0:
            now = time.time()
            uid = message.author.id
            timestamps = [t for t in image_tracker.get(uid, []) if now - t < 5]
            timestamps.append(now)
            image_tracker[uid] = timestamps
            if len(timestamps) >= 4:
                try:
                    await message.delete()
                except discord.HTTPException:
                    pass
                try:
                    await message.author.send("Do not send more than 4 images within 5 seconds.\n You are not in trouble, this is a security thing for bots that spam.")
                except discord.HTTPException:
                    pass
                try:
                    await message.author.timeout(timedelta(minutes=1), reason="Image spam rate limit triggered")
                except (discord.Forbidden, discord.HTTPException):
                    pass
                image_tracker[uid] = []


async def setup(bot):
    await bot.add_cog(Honeypot(bot))