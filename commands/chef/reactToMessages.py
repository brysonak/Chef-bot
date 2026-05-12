import discord
from discord.ext import commands
from pathlib import Path
from discord import app_commands
import random


CHANNELS = []
ASSET_PATH = Path(__file__).resolve().parents[2] / "assets" / "reactionImages"
CHANNEL_CONFIG_FILE = Path(__file__).resolve().parents[2] / "config" / "reaction_channels.txt"


class ReactToMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open(CHANNEL_CONFIG_FILE, "r") as config_file:
                for line in config_file:
                    line = line.strip()
                    if not line == "":
                        CHANNELS.append(int(line))
        except FileNotFoundError:
            with open(CHANNEL_CONFIG_FILE, "w") as config_file:
                pass
            print("Reaction channel config file not found, made a new one.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id not in CHANNELS:
            return

        if "wtf chef" in message.content.lower():
            await message.channel.send(file=discord.File(ASSET_PATH + "/image.png"), filename="wtf-chef.png")

        if "yes chef" in message.content.lower():
            await message.channel.send(file=discord.File(ASSET_PATH + "/yes-chef.png"), filename="yes-chef.png")

        if "random chef" in message.content.lower():
            valid_pictures = []
            for item in ASSET_PATH.iterdir():
                if item.is_file() and item.suffix in [".png", ".jpg", ".jpeg", ".gif"]:
                    valid_pictures.append(item)

            await message.channel.send(file=discord.File(str(random.choice(valid_pictures)), filename="yes-chef.png"))

    @app_commands.command(name="add_reaction_channel", description="Add a channel to the reaction channels list")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add_reaction_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if channel.id in CHANNELS:
            await interaction.response.send_message(f"Channel ID {channel.id} is already in the reaction channels list.", ephemeral=True)
            return

        CHANNELS.append(channel.id)
        with open(CHANNEL_CONFIG_FILE, "a") as config_file:
            config_file.write(f"{channel.id}\n")

        await interaction.response.send_message(f"Channel ID {channel.id} has been added to the reaction channels list.", ephemeral=True)

    @app_commands.command(name="remove_reaction_channel", description="Remove a channel from the reaction channels list")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def remove_reaction_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if channel.id not in CHANNELS:
            await interaction.response.send_message(f"Channel ID {channel.id} is not in the reaction channels list.", ephemeral=True)
            return

        CHANNELS.remove(channel.id)
        with open(CHANNEL_CONFIG_FILE, "w") as config_file:
            config_file.write("\n".join(str(id) for id in CHANNELS))

        await interaction.response.send_message(f"Channel ID {channel.id} has been removed from the reaction channels list.", ephemeral=True)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to run this command.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(ReactToMessages(bot))