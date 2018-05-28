"""
Charlie's Bot - Main file
"""

# TODO: Add some checks to the commands to ensure they're not empty or contain numbers

import datetime
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
    # if icao == "":
    #     await ctx.send("! You need to provide a valid 4 digit ICAO code !")
    # else:
    await ctx.send(fetch_metar_raw(icao))


@bot.command()
async def taf(ctx, icao: str):
    await ctx.send(fetch_taf_raw(icao))

# This should take the icao, source the JSON data, initialize variables in a
# class and return the class, allowing us to format our embed

@bot.command()
async def dmetar(ctx, icao: str):
    DateTime = datetime.datetime.utcnow()
    DateTime = DateTime.strftime("%Y/%m/%d %H:%M:%S")
    metar = fetch_metar_decoded(icao)

    embed=discord.Embed(title="DECODED METAR", color=0xff0000)
    # embed.set_author(name=".", url="", icon_url="http://charliedelta.co.za/uploads/images/fsx.png")
    embed.set_thumbnail(url="http://charliedelta.co.za/uploads/images/fsx.png")
    # embed.add_field(name="DECODED METAR", value='\uFEFF', inline=False)
    embed.add_field(name="ICAO", value=metar.icao, inline=True)
    embed.add_field(name="Airport", value=metar.name, inline=True)
    embed.add_field(name="Observed At", value=metar.observed, inline=False)
    embed.add_field(name="Wind / Speed", value=metar.winddir + " / " + metar.windspd + " knots", inline=False)
    # embed.add_field(name="Speed", value=metar.windspd + " knots", inline=False)
    embed.add_field(name="Visibility", value=metar.vis + " m", inline=False)
    embed.add_field(name="Clouds", value=metar.clouds, inline=False)
    embed.add_field(name="Temperature", value=metar.temp + "C | " + metar.dewp + "C", inline=False)
    # embed.add_field(name="Dewpoint", value=metar.dewp + "C", inline=False)
    embed.add_field(name="Pressure", value=metar.pressure + " hPa", inline=False)
    embed.set_footer(text="Requested at {}".format(DateTime))
    #await self.bot.say(embed=embed)

    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print('----------')
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('----------')
    game = discord.Game("!help")
    await bot.change_presence(status=discord.Status.online, activity=game)


bot.run(token)
