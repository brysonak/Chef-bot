import discord
from discord.ext import commands, tasks
from nmk_leaderboard_module import new_leaderboard_module as nmk_leader
import traceback

CHANNEL = 1503833285728669716

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.edit_leaderboard.start()
        
    @commands.command(name='update_leaderboard')
    @commands.has_permissions(manage_messages=True)
    async def update_leaderboard(self, ctx):
        e = await self.edit_leaderboard()
        if (e == 1):
            await ctx.send("Leaderboard updated!")
        else:
            await ctx.send("Leaderboard failed to update with exception " + str(e))

    @tasks.loop(minutes=1440)
    async def edit_leaderboard(self):
        try:
            edited_leaderboard = False
            leaderboard_channel = self.bot.get_channel(CHANNEL)
            # Gotta add in the class here because intellisense is fucking annoying.
            leaderboard_message = Leaderboard.generate_leaderboard_message()
            if leaderboard_message.startswith("FAILED:"):
                return leaderboard_message
            if leaderboard_channel is not None:
                async for message in leaderboard_channel.history(limit=100):
                    if message.author == self.bot.user:
                        try:
                            await message.edit(content="Todays Top Chefs:\n" + leaderboard_message)
                            edited_leaderboard = True
                        except discord.HTTPException:
                            pass
            if not edited_leaderboard and leaderboard_channel is not None:
                await leaderboard_channel.send("Todays Top Chefs:\n" + leaderboard_message)
            return 1
        except Exception as e:
            return traceback.format_exc()

    @edit_leaderboard.before_loop
    async def before_edit_leaderboard(self):
        print("Waiting for bot to be ready before starting leaderboard loop...")
        await self.bot.wait_until_ready()


    # TODO: Make this look cooler, possibly in a stylized embed or something.
    @staticmethod
    def generate_leaderboard_message():
        board = nmk_leader.extract_leaderboard_data('flappy')
        message = "Flappy Leaderboard:\n```"
        for entry in board:
            message += f"{entry["rank"]}: {entry["persona"]} - {entry["score"]}\n"
        message += "```\n\n"
        return message

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
