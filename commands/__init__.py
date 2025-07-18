from .ping import setup as setup_ping
from .lol import setup as setup_lol
from .echo import setup as setup_echo
#from .lm import setup as setup_lm

def setup_commands(bot):
    setup_ping(bot)
    setup_lol(bot)
    setup_echo(bot)
    #setup_lm(bot)