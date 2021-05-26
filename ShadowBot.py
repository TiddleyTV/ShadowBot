# ShadowBot.py

import os
import logging
import discord
import mysql.connector

from mysql.connector import MySQLConnection
from discord.ext import commands 
from dotenv import load_dotenv

from dbconfig import read_db_config
from users import *




# Set up Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Set up Intents
intents = discord.Intents.all()


# Load the bot's Discord Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(f'{TOKEN} has connected to Discord!')


# Setup a mysql DB Connection
dbconfig = read_db_config()
conn = MySQLConnection(**dbconfig)
if conn.is_connected():
	print("Database Connection Successful.")
else:
	print("Database Connection Failed.")
	exit;
conn.autocommit = True
cursor = conn.cursor()




# Setup Command Prefix
bot = commands.Bot(command_prefix='!sb ', intents = intents)

@bot.command(name='echo', help='Echos the message back to a user')
async def echo(ctx, *args):
	# Echo the message back to the user 
	response = ""
	for arg in args:
		response = response + " " + arg
	response = ctx.message.content
	response = response.replace('!sb echo', '', 1)
	await ctx.send(response)


@bot.command(name='setmain', help='Set the users WoW Main')
async def setmain(ctx, wowmain=None, userid: discord.Member=None):
	if userid is None:
		userid = ctx.message.author
	author = ctx.message.author
	guild = ctx.message.guild

	# A user can set their own wow main.
	# An admin can set anybodies wow main.

	# First arg should be a wow character name.
	if wowmain is None:
		response = "Usage: \n!sb setmain <wow character name>\n"
		response = response + "Admin Only\n!sb setmain <wow character name> <discord name>\n"
		await ctx.send(response)
	else:
		# Second Arg should be a username.  If its set in the command, make sure
		# the author has permissions

		# If userid and author are different, require permissions
		if author is userid:
			set_wow_main(cursor,guild,userid,wowmain)
			mention = userid.mention
			response = f"WoW Main for {userid.mention} set to {wowmain}"
			await ctx.send(response)
		else:
			# Check for permission
			set_wow_main(cursor,guild,userid,wowmain)
			response = f"Admin: WoW Main for {userid.mention} set to {wowmain}"
			await ctx.send(response)

@bot.command(name='getmain', help='Get the users WoW Main')
async def getmain(ctx, wowmain=None, userid: discord.Member=None):
	if userid is None:
		userid = ctx.message.author
	guild = ctx.message.guild
	wowmain = get_wow_main(cursor,guild,userid)
	if wowmain is None:
		response = f"{userid.mention}'s WoW main is not known."
	else:
		response = f"{userid.mention}'s WoW main is {wowmain}."
	await ctx.send(response)



@bot.command(name='apply', help='Apply To Join')
async def apply(ctx, *args):
	channel = ctx.channel.name
	if channel != 'applications':
		await ctx.send("That command does not work here.")
		return
	await ctx.send("Apply")

@bot.event
async def on_ready():
	print(f'{bot.user} is connected to the following guilds:')
	for guild in bot.guilds:
		print(f'{guild.name}(id: {guild.id})')

@bot.event
async def on_member_update(before,after):
	guild = after.guild
	userid = str(after.name) + "#" + str(after.discriminator)
	update_user_seen(cursor,guild,userid)

	
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	guild = message.guild
	userid = message.author
	if check_user_exists(cursor,guild,userid) is False:
		add_user(cursor,userid)
	else: 
		update_user_seen(cursor,guild,userid)

	# Add this or the bot doesn't execute any commands
	await bot.process_commands(message)


bot.run(TOKEN)
