import discord
from discord.ext import commands
# Use these for prefix commands, not slash commands.

def is_mod():
    async def predicate(ctx):
        if isinstance(ctx.author, discord.Member):
            return ctx.author.guild_permissions.manage_messages or ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_channels
        return False
    return commands.check(predicate)


def is_owner():
    async def predicate(ctx):
        if isinstance(ctx.author, discord.Member):
            return ctx.author.id == ctx.guild.owner_id
        return False
    return commands.check(predicate)


def is_bot_owner():
    return commands.is_owner()


def is_mod_or_higher():
    async def predicate(ctx):
        if isinstance(ctx.author, discord.Member):
            perms = ctx.author.guild_permissions
            return perms.manage_messages or perms.administrator or ctx.author.id == ctx.guild.owner_id or await ctx.bot.is_owner(ctx.author)
        return False
    return commands.check(predicate)