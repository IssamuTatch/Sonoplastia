from .on_ready import setup as setup_ready
from .on_voice_state_update import setup as setup_voice_state_update

def setup_events(bot):
    setup_ready(bot)
    setup_voice_state_update(bot)