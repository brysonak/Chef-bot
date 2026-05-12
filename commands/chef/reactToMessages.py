import discord
from discord.ext import commands
from pathlib import Path
from discord import app_commands


CHANNELS = []
ASSET_PATH = Path(__file__).resolve().parents[2] / "assets" / "yes-chef.png"
CHANNEL_CONFIG_FILE = Path(__file__).resolve().parents[2] / "config" / "reaction_channels.txt"


class ReactToMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(CHANNEL_CONFIG_FILE, "r") as config_file:
            for line in config_file:
                line = line.strip()
                if not line == "":
                    CHANNELS.append(int(line))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id not in CHANNELS:
            return

        if "yes chef" not in message.content.lower():
            return

        await message.channel.send(file=discord.File(str(ASSET_PATH), filename="yes-chef.png"))

    @app_commands.command(name="add_reaction_channel", description="Add a channel to the reaction channels list")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add_reaction_channel(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        if channel_id in CHANNELS:
            await ctx.send(f"Channel ID {channel_id} is already in the reaction channels list.")
            return

        CHANNELS.append(channel_id)
        with open(CHANNEL_CONFIG_FILE, "a") as config_file:
            config_file.write(f"{channel_id}\n")

        await ctx.send(f"Channel ID {channel_id} has been added to the reaction channels list.")

    @app_commands.command(name="remove_reaction_channel", description="Remove a channel from the reaction channels list")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def remove_reaction_channel(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        if not channel_id in CHANNELS:
            await ctx.send(f"Channel ID {channel_id} is not in the reaction channels list.")
            return

        CHANNELS.remove(channel_id)
        with open(CHANNEL_CONFIG_FILE, "w") as config_file:
            config_file.write("\n".join(str(id) for id in CHANNELS))

        await ctx.send(f"Channel ID {channel_id} has been removed from the reaction channels list.")



async def setup(bot):
    await bot.add_cog(ReactToMessages(bot))