# ShadowBot.py

import os
import logging

from discord.ext import commands 
from dotenv import load_dotenv

# Set up Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Load the bot's Discord Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(f'{TOKEN} has connected to Discord!')

bot = commands.Bot(command_prefix='!sb ')

@bot.command(name='echo', help='Echos the message back to a user')
async def echo(ctx, *args):
	# Echo the message back to the user 
	response = ""
	for arg in args:
		response = response + " " + arg
	await ctx.send(response)

@bot.event
async def on_ready():
	print(f'{bot.user} is connected to the following guilds:')
	for guild in bot.guilds:
		print(f'{guild.name}(id: {guild.id})')

bot.run(TOKEN)
