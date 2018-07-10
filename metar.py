"""
METAR Fetch and Decode module, hopefully to be used in a Discord Bot
Data provided by http://checkwx.com via API
"""


import requests
from credentials import key
headers = { 'X-API-Key': key }


class Metar:
    def __init__(self, metar, clouds2=None, clouds3=None, clouds4=None, clouds5=None, length=1):
        self.icao = metar[0]['icao']
        self.name = metar[0]['name']
        self.observed = metar[0]['observed']
        self.winddir = str(metar[0]['wind']['degrees'])
        self.windspd = str(metar[0]['wind']['speed_kts'])
        self.vis = str(metar[0]['visibility']['meters'])
        # This may need some looking at for multiple cloud reports
        self.clouds = metar[0]['clouds'][0]['text']
        self.clouds2 = clouds2
        self.clouds3 = clouds3
        self.clouds4 = clouds4
        self.clouds5 = clouds5
        self.temp = str(metar[0]['temperature']['celsius'])
        self.dewp = str(metar[0]['dewpoint']['celsius'])
        self.pressure = str(metar[0]['barometer']['mb'])
        self.temp_alt = str(metar[0]['temperature']['fahrenheit'])
        self.dewp_alt = str(metar[0]['dewpoint']['fahrenheit'])
        self.pressure_alt = str(metar[0]['barometer']['hg'])
        self.length = length


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
    metar_resp = response.json()
    metar = metar_resp.get('data')
    return(metar[0])


def fetch_metar_decoded(icao):  #Try this as an embed? Or pre formatted string
    url = 'https://api.checkwx.com/metar/{}/decoded'.format(icao)
    response = requests.get(url, headers=headers)
    metar_resp = response.json()
    metar = metar_resp.get('data')
    #print(metar)
    length = len(metar[0]['clouds'])
    # This is horrible, but does it work?
    if length == 1:
        embed = Metar(metar)
    elif length == 2:
        clouds2 = metar['data'][0]['clouds'][1]

        embed = Metar(metar,clouds2,length)
    elif length == 3:
        clouds2 = metar['data'][0]['clouds'][1]
        clouds3 = metar['data'][0]['clouds'][2]

        embed = Metar(metar,clouds2,clouds3,length)
    elif length == 4:
        clouds2 = metar['data'][0]['clouds'][1]
        clouds3 = metar['data'][0]['clouds'][2]
        clouds4 = metar['data'][0]['clouds'][3]

        embed = Metar(metar,clouds2,clouds3,clouds4,length)
    elif length == 5:
        clouds2 = metar['data'][0]['clouds'][1]
        clouds3 = metar['data'][0]['clouds'][2]
        clouds4 = metar['data'][0]['clouds'][3]
        clouds5 = metar['data'][0]['clouds'][4]

        embed = Metar(metar,clouds2,clouds3,clouds4,clouds5,length)
    else:
        raise Exception('More than 5 cloud reports! Unable to parse')

    return embed


def fetch_taf_raw(icao):
    url = 'https://api.checkwx.com/taf/{}'.format(icao)
    response = requests.get(url, headers=headers)
    taf_resp = response.json()
    taf = taf_resp.get('data')
    return(taf[0])


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
