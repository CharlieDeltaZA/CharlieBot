"""
METAR Fetch and Decode module, hopefully to be used in a Discord Bot
Data provided by http://checkwx.com via API
"""


import requests
from credentials import key
headers = { 'X-API-Key': key }


class Metar:
    def __init__(self, metar):
        self.icao = metar['data'][0]['icao']
        self.name = metar['data'][0]['name']
        self.observed = metar['data'][0]['observed']
        self.winddir = metar['data'][0]['wind']['degrees']
        self.windspd = str(metar['data'][0]['wind']['speed_kts'])
        self.vis = str(metar['data'][0]['visibility']['meters'])
        # This may need some looking at for multiple cloud reports
        self.clouds = metar['data'][0]['clouds'][0]['text']
        self.temp = str(metar['data'][0]['temperature']['celsius'])
        self.dewp = str(metar['data'][0]['dewpoint']['celsius'])
        self.pressure = str(metar['data'][0]['barometer']['mb'])


# Shouldn't need a main unless I run it from command line, but we'll include
# it just for safety sake
def main():
    cmd, icao = get_inputs()

    if icao:
        if cmd == 'f':
            print('Fetching RAW METAR...')
            metar = fetch_metar_raw(icao)
            print(metar)
        elif cmd == 'd':
            print('Fetching Decoded METAR...')
            #metar = fetch_metar_decoded(icao)
            fetch_metar_decoded(icao)
            #print(metar)
        elif cmd == 't':
            print('Fetching TAF...')
            taf = fetch_taf_raw(icao)
            print(taf)
        else:
            print('Exiting...')
            pass
    else:
        print('You must specify an airport!')


def fetch_metar_raw(icao):
    url = 'https://api.checkwx.com/metar/{}'.format(icao)
    response = requests.get(url, headers=headers)
    metar = response.json()
    return(metar['data'][0])


def fetch_metar_decoded(icao):  #Try this as an embed? Or pre formatted string
    url = 'https://api.checkwx.com/metar/{}/decoded'.format(icao)
    response = requests.get(url, headers=headers)
    metar = response.json()
    #print(metar)
    embed = Metar(metar)
    return embed


def fetch_taf_raw(icao):
    url = 'https://api.checkwx.com/taf/{}'.format(icao)
    response = requests.get(url, headers=headers)
    taf = response.json()
    return(taf['data'][0])


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
