import discord
from discord.ext import commands, tasks
from nmk_leaderboard_module import nmk_leaderboards as nmk_leader

CHANNEL = 1503833285728669716

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @tasks.loop(minutes=1440)
    async def edit_leaderboard(self):
        edited_leaderboard = False
        leaderboard_channel = self.bot.get_channel(CHANNEL)

        leaderboard_message = generate_leaderboard_message()

        if leaderboard_channel is not None:
            for message in leaderboard_channel.history(limit=100):
                if message.author == self.bot.user:
                    try:
                        await message.edit(content="Todays Top Players:\n" + leaderboard_message)
                        edited_leaderboard = True
                    except discord.HTTPException:
                        pass
        if not edited_leaderboard:
            await leaderboard_channel.send("Todays Top Players:\n" + leaderboard_message)

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


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
    await Leaderboard.edit_leaderboard.start()