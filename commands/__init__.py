from .ping import setup as setup_ping
from .lol import setup as lolhistory

def setup_commands(bot):
    setup_ping(bot)
    lolhistory(bot)