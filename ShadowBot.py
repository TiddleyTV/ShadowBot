# ShadowBot.py

import os
import discord
import logging
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

client = discord.Client()

@client.event
async def on_ready():
	print(f'{client.user} is connected to the following guilds:')
	for guild in client.guilds:
		print(f'{guild.name}(id: {guild.id})')

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	# Base Trigger.  Send Help Message
	if message.content == '!sb':
		await message.channel.send('Hello!')

	# Echo the message back to the user 
	if message.content.startswith('!sb echo'):
		new_message = message.content.replace('!sb echo', '', 1)
		await message.channel.send(new_message)

client.run(TOKEN)
