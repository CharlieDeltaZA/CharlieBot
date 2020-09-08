"""
METAR Fetch and Decode module, hopefully to be used in a Discord Bot
Data provided by http://checkwx.com via API
"""


import requests
from credentials import key
headers = { 'X-API-Key': key }


class Metar:
    def __init__(self, metar,
    c2="", c3="", c4="", c5="",
    c2_alt="", c3_alt="", c4_alt="", c5_alt="",
    length=1):

        self.icao = metar[0]['icao']
        self.name = metar[0]['station']['name']
        self.observed = metar[0]['observed']
        self.winddir = str(metar[0]['wind']['degrees'])
        self.windspd = str(metar[0]['wind']['speed_kts'])
        self.vis = str(metar[0]['visibility']['meters'])
        # This may need some looking at for multiple cloud reports

        self.clouds = metar[0]['clouds'][0]['text']
        self.clouds2 = c2
        self.clouds3 = c3
        self.clouds4 = c4
        self.clouds5 = c5
        self.clouds_alt = str(metar[0]['clouds'][0]['feet'])
        self.clouds2_alt = str(c2_alt)
        self.clouds3_alt = str(c3_alt)
        self.clouds4_alt = str(c4_alt)
        self.clouds5_alt = str(c5_alt)

        self.temp = str(metar[0]['temperature']['celsius'])
        self.dewp = str(metar[0]['dewpoint']['celsius'])
        self.pressure = str(metar[0]['barometer']['mb'])
        self.temp_alt = str(metar[0]['temperature']['fahrenheit'])
        self.dewp_alt = str(metar[0]['dewpoint']['fahrenheit'])
        self.pressure_alt = str(metar[0]['barometer']['hg'])
        self.length = length
        self.skycond = metar[0]['clouds'][0]['code']


# Shouldn't need a main unless I run it from command line, but we'll include
# it just for safety sake
def main():
    cmd, icao = get_inputs()

    if icao:
        if cmd == 'f':
            print('Fetching RAW METAR...')
            metar = fetchMetarRaw(icao)
            print(metar)
        elif cmd == 'd':
            print('Fetching Decoded METAR...')
            #metar = fetch_metar_decoded(icao)
            fetch_metar_decoded(icao)
            #print(metar)
        elif cmd == 't':
            print('Fetching TAF...')
            taf = fetchTafRaw(icao)
            print(taf)
        else:
            print('Exiting...')
            pass
    else:
        print('You must specify an airport!')

def fetchStationInfo(icao):
    url = 'https://api.checkwx.com/station/{}'.format(icao)
    response = requests.get(url, headers=headers)
    stationResp = response.json()
    # print(stationResp)
    if stationResp['results'] == 1:
        # print("")
        # print(type(stationResp['data'][0]))
        station = stationResp['data'][0]
        return(station)
    else:
        return("No station info available for {}".format(icao.upper()))
    

def fetchTafRaw(icao):
    url = 'https://api.checkwx.com/taf/{}'.format(icao)
    response = requests.get(url, headers=headers)
    tafResp = response.json()
    if tafResp['results'] == 1:
        taf = tafResp['data'][0]
        return(taf)
    else:
        return("No taf available for {}".format(icao.upper()))


def fetchMetarRaw(icao):
    url = 'https://api.checkwx.com/metar/{}'.format(icao)
    response = requests.get(url, headers=headers)
    metarResp = response.json()
    if metarResp['results'] == 1:
        metar = metarResp['data'][0]
        return(metar)
    else:
        return("No metar available for {}".format(icao.upper()))


def fetch_metar_decoded(icao):  #Try this as an embed? Or pre formatted string
    url = 'https://api.checkwx.com/metar/{}/decoded'.format(icao)
    response = requests.get(url, headers=headers)
    metar_resp = response.json()
    metar = metar_resp.get('data')
    #print(metar)
    length = len(metar[0]['clouds'])
    embed, clouds_emb = determine_clouds(length, metar)

    return embed, clouds_emb


# This is horrible, but does it work?
def determine_clouds(length, metar):
    length = length
    metar = metar

    if length == 1:
        embed = Metar(metar)
        skycond = metar[0]['clouds'][0]['code']
        if skycond in { 'CLR', 'CAVOK', 'NSC', 'NCD', 'SKC' }:
            clouds_emb = metar[0]['clouds'][0]['text']
        else:
            clouds_emb = '{} {}ft AGL'.format(metar[0]['clouds'][0]['text'],
            metar[0]['clouds'][0]['feet'])

    elif length == 2:
        clouds2 = metar[0]['clouds'][1]['text']
        c2_alt= metar[0]['clouds'][1]['feet']

        embed = Metar(metar,c2=clouds2,c2_alt=c2_alt,length=length)

    elif length == 3:
        clouds2 = metar[0]['clouds'][1]['text']
        clouds3 = metar[0]['clouds'][2]['text']
        c2_alt= metar[0]['clouds'][1]['feet']
        c3_alt= metar[0]['clouds'][2]['feet']

        embed = Metar(metar,c2=clouds2,c3=clouds3,c2_alt=c2_alt,c3_alt=c3_alt,
        length=length)

    elif length == 4:
        clouds2 = metar[0]['clouds'][1]['text']
        clouds3 = metar[0]['clouds'][2]['text']
        clouds4 = metar[0]['clouds'][3]['text']
        c2_alt= metar[0]['clouds'][1]['feet']
        c3_alt= metar[0]['clouds'][2]['feet']
        c4_alt= metar[0]['clouds'][3]['feet']

        embed = Metar(metar,c2=clouds2,c3=clouds3,c4=clouds4,c2_alt=c2_alt,
        c3_alt=c3_alt,c4_alt=c4_alt,length=length)

    elif length == 5:
        clouds2 = metar[0]['clouds'][1]['text']
        clouds3 = metar[0]['clouds'][2]['text']
        clouds4 = metar[0]['clouds'][3]['text']
        clouds5 = metar[0]['clouds'][4]['text']
        c2_alt= metar[0]['clouds'][1]['feet']
        c3_alt= metar[0]['clouds'][2]['feet']
        c4_alt= metar[0]['clouds'][3]['feet']
        c5_alt= metar[0]['clouds'][4]['feet']

        embed = Metar(metar,c2=clouds2,c3=clouds3,c4=clouds4,c5=clouds5,
        c2_alt=c2_alt,c3_alt=c3_alt,c4_alt=c4_alt,c5_alt=c5_alt,
        length=length)

    else:
        raise Exception('More than 5 cloud reports! Unable to parse')

    return embed, clouds_emb


def get_inputs():
    cmd = input(
'''[F]etch METAR
[D]ecoded METAR
[T]AF
[X] to Exit
What would you like to do? ''')
    icao = input('Enter ICAO: ')
    icao = icao.lower().strip()
    cmd = cmd.lower().strip()
    return(cmd, icao)


if __name__ == '__main__':
    main()
