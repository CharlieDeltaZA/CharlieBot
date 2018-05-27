"""
Charlie's Bot - Main file
"""

# import datetime
import logging
import discord
from discord.ext import commands
from credentials import token
import metar


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix='!', description="Charlie's Bitch")


@bot.event
async def on_ready():
    game = discord.Game("Loading...")
    await bot.change_presence(status=discord.Status.dnd, activity=game)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    game = discord.Game("!help")
    await bot.change_presence(status=discord.Status.online, activity=game)


bot.run(token)
