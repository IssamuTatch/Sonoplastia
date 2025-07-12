from discord.ext import commands

def setup(bot):
    @bot.command()
    async def ping(ctx):
        await ctx.send("pong")