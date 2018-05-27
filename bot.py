"""
Charlie's Bot - Main file
"""

# import datetime
import logging
import discord
from discord.ext import commands
from credentials import token
from metar import fetch_taf_raw, fetch_metar_raw, fetch_metar_decoded


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix='!', description="Charlie's Bitch")

@bot.command()
async def metar(ctx, icao: str):
    await ctx.send(fetch_metar_raw(icao))


@bot.command()
async def taf(ctx, icao: str):
    await ctx.send(fetch_taf_raw(icao))


#@bot.command()
#async def dmetar(ctx, icao: str):
#    await ctx.send(fetch_metar_decoded(icao))


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
