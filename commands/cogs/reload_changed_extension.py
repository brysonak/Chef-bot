import discord
from discord import app_commands
from discord.ext import commands

class ReloadChangedExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload_extension", description="Reload a bot extension")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def reload_extension(self, interaction: discord.Interaction, extension: str):
        try:
            await self.bot.reload_extension(extension)
            await interaction.response.send_message(f"Extension '{extension}' reloaded successfully.")
        except Exception as e:
            await interaction.response.send_message(f"Failed to reload extension '{extension}': {e}")

    @reload_extension.error
    async def reload_extension_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(ReloadChangedExtension(bot))