import discord
from discord.ext import commands
from discord import app_commands
import pytz
from datetime import datetime

TICKET_CATEGORY = 1235871701829550080


class CloseWithReasonModal(discord.ui.Modal, title="Close Ticket"):
    reason = discord.ui.TextInput(label="Reason for closing", style=discord.TextStyle.paragraph, required=True)

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.cog.close_ticket(interaction.channel, interaction.user, self.reason.value)


class TicketView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, custom_id="ticket_close")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not (interaction.user.guild_permissions.manage_messages or interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
            await interaction.response.send_message("Only moderators can close tickets.", ephemeral=True)
            return
        await interaction.response.defer()
        await self.cog.close_ticket(interaction.channel, interaction.user, None)

    @discord.ui.button(label="Close with Reason", style=discord.ButtonStyle.secondary, custom_id="ticket_close_reason")
    async def close_with_reason_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not (interaction.user.guild_permissions.manage_messages or interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
            await interaction.response.send_message("Only moderators can close tickets.", ephemeral=True)
            return
        await interaction.response.send_modal(CloseWithReasonModal(self.cog))


class TicketCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_counter = 0
        self.open_tickets = {}

    def next_ticket_number(self):
        self.ticket_counter += 1
        return self.ticket_counter

    @app_commands.command(name="ticket-create", description="Create a support ticket")
    async def ticket_create(self, interaction: discord.Interaction, reason: str):
        guild = interaction.guild
        category = guild.get_channel(TICKET_CATEGORY)

        ticket_number = self.next_ticket_number()
        channel_name = f"ticket-{ticket_number}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }
        for role in guild.roles:
            if role.permissions.manage_messages or role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        est = pytz.timezone("America/New_York")
        opened_at = datetime.now(est)

        self.open_tickets[channel.id] = {
            "opener": interaction.user,
            "reason": reason,
            "opened_at": opened_at,
            "participants": {interaction.user.id: interaction.user},
        }

        embed = discord.Embed(title=f"Ticket #{ticket_number}", color=discord.Color.blurple())
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text="A mod will be with you as soon as possible, please be patient!")

        view = TicketView(self)
        await channel.send(embed=embed, view=view)

        await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id in self.open_tickets:
            self.open_tickets[message.channel.id]["participants"][message.author.id] = message.author

    async def close_ticket(self, channel: discord.TextChannel, closer: discord.Member, close_reason: str | None):
        ticket_data = self.open_tickets.get(channel.id)
        if not ticket_data:
            return

        est = pytz.timezone("America/New_York")
        closed_at = datetime.now(est)
        opened_at = ticket_data["opened_at"]

        participants = list(ticket_data["participants"].values())
        participant_names = ", ".join(m.display_name for m in participants)

        embed = discord.Embed(title="Ticket Closed", color=discord.Color.red())
        embed.add_field(name="Opened", value=opened_at.strftime("%Y-%m-%d %I:%M %p EST"), inline=True)
        embed.add_field(name="Closed", value=closed_at.strftime("%Y-%m-%d %I:%M %p EST"), inline=True)
        embed.add_field(name="Opened By", value=ticket_data["opener"].display_name, inline=False)
        embed.add_field(name="Participants", value=participant_names or "None", inline=False)
        embed.add_field(name="Open Reason", value=ticket_data["reason"], inline=False)
        embed.add_field(name="Close Reason", value=close_reason or "No reason specified", inline=False)

        for member in participants:
            try:
                await member.send(embed=embed)
            except discord.HTTPException:
                pass

        del self.open_tickets[channel.id]
        await channel.delete()


async def setup(bot):
    await bot.add_cog(TicketCreate(bot))