import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from commands import setup_commands
from events import setup_events

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='>', intents=intents)

setup_events(bot)

setup_commands(bot)

bot.run(BOT_TOKEN)
