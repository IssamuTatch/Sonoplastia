def setup(bot):
    @bot.event
    async def on_ready():
        print(f'Bot connected as {bot.user}')