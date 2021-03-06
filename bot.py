"""
Charlie's Bot - Main file
"""

# TODO: Add some checks to the commands to ensure they're not empty or contain numbers

import datetime
import logging
import discord
from discord.ext import commands
from credentials import token
from benedict import benedict
from metar import fetchTafRaw, fetchMetarRaw, fetch_metar_decoded, fetchStationInfo


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot(command_prefix='!', description="Charlie's Little Helper")


@bot.command()
async def metar(ctx, icao: str):
    metar = fetchMetarRaw(icao)
    station = fetchStationInfo(icao)

    if (type(station) != type(dict())):
        await ctx.send(metar)
    else:
        station = benedict(station)
        countryName = station['country.name'] if 'country.name' in station else 'Unknown Country'
        city = station['city'] if 'city' in station else 'Unknown City'
        elevation = station['elevation.feet'] if 'elevation.feet' in station else 'Unknown Elevation'

        metarEmbed = discord.Embed(
            title = 'Metar & Station Info - ' + icao.upper(),
            # description = icao,
            colour = discord.Colour.red()
        )

        # metarEmbed.set_author(name=station['name'])
        metarEmbed.add_field(name="Raw Metar", value=metar, inline=False)

        metarEmbed.add_field(name="Name", value=station['name'], inline=True)
        metarEmbed.add_field(name="City", value=city, inline=True)
        metarEmbed.add_field(name="Country", value=countryName, inline=True)

        metarEmbed.add_field(name="Elevation", value=str(elevation) + 'ft', inline=True)
        metarEmbed.add_field(name="Latitude", value=station['latitude.decimal'], inline=True)
        metarEmbed.add_field(name="Longitude", value=station['longitude.decimal'], inline=True)


        await ctx.send(embed=metarEmbed)


@bot.command()
async def taf(ctx, icao: str):
    await ctx.send(fetchTafRaw(icao))

@bot.command()
async def icao(ctx, icao: str):
    fetchStationInfo(icao)
    await ctx.send("Check Terminal!")

# This should take the icao, source the JSON data, initialize variables in a
# class and return the class, allowing us to format our embed


@bot.command()
async def dmetar(ctx, icao: str):
    DateTime = datetime.datetime.utcnow()
    DateTime = DateTime.strftime("%d/%m/%Y %H:%M")
    metar, clouds_emb = fetch_metar_decoded(icao)

    embed = discord.Embed(title="DECODED METAR", color=0xff0000)
    # embed.set_author(name=".", url="", icon_url="http://charliedelta.co.za/uploads/images/fsx.png")
    embed.set_thumbnail(url="http://charliedelta.co.za/uploads/images/fsx.png")
    # embed.add_field(name="DECODED METAR", value='\uFEFF', inline=False)
    embed.add_field(name="ICAO", value=metar.icao, inline=True)
    embed.add_field(name="Airport", value=metar.name, inline=True)
    embed.add_field(name="Observed At", value=metar.observed, inline=False)
    embed.add_field(name="Wind / Speed", value=metar.winddir + "° / " + metar.windspd + " knots", inline=False)
    # embed.add_field(name="Speed", value=metar.windspd + " knots", inline=False)
    embed.add_field(name="Visibility", value=metar.vis + " m", inline=False)
    embed.add_field(name="Clouds",
    # value="{} {}ft AGL\n".format(metar.clouds, metar.clouds_alt)
    # + "{} {}ft AGL\n".format(metar.clouds2, metar.clouds2_alt)
    # + "{} {}ft AGL\n".format(metar.clouds3, metar.clouds3_alt)
    # + "{} {}ft AGL\n".format(metar.clouds4, metar.clouds4_alt)
    # + "{} {}ft AGL\n".format(metar.clouds5, metar.clouds5_alt),
    value=clouds_emb,
    inline=False)
    embed.add_field(name="Temperature", value=metar.temp + "°C | " + metar.dewp + "°C\n"
    + metar.temp_alt + "°F | " + metar.dewp_alt + "°F", inline=False)
    # embed.add_field(name="Dewpoint", value=metar.dewp + "C", inline=False)
    embed.add_field(name="Pressure", value=metar.pressure + " hPa\n" + metar.pressure_alt + " In", inline=False)
    embed.set_footer(text="Requested at {}Z".format(DateTime))
    # await self.bot.say(embed=embed)

    await ctx.send(content=None, embed=embed)


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
