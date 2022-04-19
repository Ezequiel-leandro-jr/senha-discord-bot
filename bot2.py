#!/usr/bin/env python

# TODO: allow admin to configure spreadsheet id

from discord.ext import commands
import discord
from database import DatabaseHelper
from spreadsheet_helper import SpreadsheetHelper
from cmd_config import ConfigCmd
from cmd_hands import HandsCmd
from cmd_student import StudentCmd
from cmd_team import TeamCmd
import os

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DATABASE_URL = os.getenv('DATABASE_URL') or 'postgres://postgres:1234@localhost:5432/postgres'
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

# docker kill postgres; docker run --rm --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=1234 -d postgres
db = DatabaseHelper(DATABASE_URL)
db.connect()
db.run_migrations()

spreadsheet_helper = SpreadsheetHelper(GOOGLE_SERVICE_ACCOUNT_JSON)

async def on_ready():
    print('Bot is online')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)
bot.db = db
bot.spreadsheet = spreadsheet_helper
bot.add_cog(HandsCmd(bot))
bot.add_cog(ConfigCmd(bot))
bot.add_cog(StudentCmd(bot))
bot.add_cog(TeamCmd(bot))
print('Starting bot...')
bot.add_listener(on_ready)
bot.run(DISCORD_BOT_TOKEN)

