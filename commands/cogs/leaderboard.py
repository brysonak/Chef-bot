import discord
from discord.ext import commands, tasks
from nmk_leaderboard_module import nmk_leaderboards as nmk_leader

CHANNEL = 1503833285728669716

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.edit_leaderboard.start()
        
    @commands.command(name='update_leaderboard')
    @commands.has_permissions(manage_messages=True)
    async def update_leaderboard(self, ctx):
        await self.edit_leaderboard()
        await ctx.send("Leaderboard updated!")

    @tasks.loop(minutes=1440)
    async def edit_leaderboard(self):
        edited_leaderboard = False
        leaderboard_channel = self.bot.get_channel(CHANNEL)
        # Gotta add in the class here because intellisense is fucking annoying.
        leaderboard_message = Leaderboard.generate_leaderboard_message()

        if leaderboard_channel is not None:
            async for message in leaderboard_channel.history(limit=100):
                if message.author == self.bot.user:
                    try:
                        await message.edit(content="Todays Top Chefs:\n" + leaderboard_message)
                        edited_leaderboard = True
                    except discord.HTTPException:
                        pass
        if not edited_leaderboard:
            await leaderboard_channel.send("Todays Top Chefs:\n" + leaderboard_message)

    @staticmethod
    def generate_leaderboard_message():
        board = nmk_leader.query_board_top('flappy', top_count=10)
        message = "Flappy Leaderboard:\n```"
        for entry in board:
            message += f"{entry.rank}: {entry.persona} - {entry.score}\n"
        message += "```\n\n"

        board = nmk_leader.query_board_top('stack', top_count=10)
        message += "Stack Leaderboard:\n```"
        for entry in board:
            message += f"{entry.rank}: {entry.persona} - {entry.score}\n"
        message += "```\n\n"

        board = nmk_leader.query_board_top('rope', top_count=10)
        message += "Rope Leaderboard:\n```"
        for entry in board:
            message += f"{entry.rank}: {entry.persona} - {entry.score}\n"
        message += "```"

        return message


    async def cog_unload(self):
        self.edit_leaderboard.cancel()


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
