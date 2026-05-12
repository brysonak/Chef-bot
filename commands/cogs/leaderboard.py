import discord
from discord.ext import commands, tasks


CHANNEL = 1503833285728669716

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @tasks.loop(minutes=1440)
    async def edit_leaderboard(self):
        edited_leaderboard = False
        leaderboard_channel = self.bot.get_channel(CHANNEL)
        if leaderboard_channel is not None:
            for message in leaderboard_channel.history(limit=100):
                if message.author == self.bot.user:
                    try:
                        await message.edit()
                        edited_leaderboard = True
                    except discord.HTTPException:
                        pass
        if not edited_leaderboard:
            await leaderboard_channel.send()


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
    await Leaderboard.edit_leaderboard.start()