import discord
from discord.ext import commands
from discord import app_commands


class TicketRename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket-rename", description="[MOD ONLY] Rename the current ticket channel")
    async def ticket_rename(self, interaction: discord.Interaction, name: str):
        if not (interaction.user.guild_permissions.manage_messages or interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
            await interaction.response.send_message("Only moderators can rename tickets.", ephemeral=True)
            return

        ticket_cog = self.bot.cogs.get("TicketCreate")
        if not ticket_cog or interaction.channel_id not in ticket_cog.open_tickets:
            await interaction.response.send_message("This channel is not an open ticket.", ephemeral=True)
            return

        await interaction.channel.edit(name=name)
        await interaction.response.send_message(f"Ticket renamed to `{name}`.")


async def setup(bot):
    await bot.add_cog(TicketRename(bot))