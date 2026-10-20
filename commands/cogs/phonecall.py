import re
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from rotary import *
import random


class Phonecall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_in_specific_channel(interaction: discord.Interaction) -> bool:
            return interaction.channel_id == 1562228814816481370

    
    @app_commands.command(name="phonecall", description="Try to deduce the phone number")
    @app_commands.check(is_in_specific_channel)
    async def phonecallCommand(self, interaction: discord.Interaction):
        inputStr = ""
        await interaction.response.defer()
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel

        initializeGame()
        await interaction.channel.send(f"You are trying to track down a phone number. Your only lead is that you can reach one of his friends at {phoneNumber1}\nPhone numbers are always expected as XXX-XXX-XXXX format.")
        while not inputStr == "exit":
            try:
                await interaction.channel.send("What phone number would you like to dial? You only need the phone number")
                msg = await self.bot.wait_for('message', check=check, timeout=300.0)
                inputStr = msg.content.strip()
            except asyncio.TimeoutError:
                inputStr = "exit"
                await interaction.channel.send("Sorry, you took too long to answer!")
                
            if (inputStr == phoneNumber1):
               await interaction.channel.send(giveLocation(phoneNumber2))
            elif (inputStr == phoneNumber2):
                await interaction.channel.send(givePrefix(phoneNumber3))
            elif (inputStr == phoneNumber3):
                await interaction.channel.send(giveLine())
            elif (inputStr == phoneNumber):
                await interaction.channel.send("You Win! You sucessfully called him about his car's extended warranty!")
                inputStr = "exit"
            elif (not inputStr == "exit"):
                await interaction.channel.send(random.choice(wrongNumberStrings))

    @phonecallCommand.error
    async def phonecallCommand_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(
                "You cannot use this command in this channel.", 
                ephemeral=True # Makes the error message visible only to the user
            )



async def setup(bot):
    await bot.add_cog(Phonecall(bot))