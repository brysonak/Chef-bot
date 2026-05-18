import discord
from discord.ext import commands
from discord import app_commands


class TicketAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket-add", description="[MOD ONLY] Give a user access to the current ticket")
    async def ticket_add(self, interaction: discord.Interaction, user: discord.Member):
        if not (interaction.user.guild_permissions.manage_messages or interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
            await interaction.response.send_message("Only moderators can add users to tickets.", ephemeral=True)
            return

        ticket_cog = self.bot.cogs.get("TicketCreate")
        if not ticket_cog or interaction.channel_id not in ticket_cog.open_tickets:
            await interaction.response.send_message("This channel is not an open ticket.", ephemeral=True)
            return

        await interaction.channel.set_permissions(user, view_channel=True, send_messages=True, read_message_history=True)
        ticket_cog.open_tickets[interaction.channel_id]["participants"][user.id] = user
        await interaction.response.send_message(f"{user.mention} has been added to the ticket.")


async def setup(bot):
    await bot.add_cog(TicketAdd(bot))