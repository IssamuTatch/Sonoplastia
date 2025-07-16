def setup(bot):
    @bot.command()
    async def echo(ctx, *args):
        await ctx.send(ctx.message.content[5:])