"""
METAR Fetch and Decode module, hopefully to be used in a Discord Bot
"""


import requests
from credentials import key
headers = { 'X-API-Key': key }

# Shouldn't need a main unless I run it from command line, but we'll include it just for safety sake
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
    print(metar)
    #return(metar['data'][0])


def fetch_taf_raw(icao):
    url = 'https://api.checkwx.com/taf/{}'.format(icao)
    response = requests.get(url, headers=headers)
    taf = response.json()
    return(taf['data'][0])


#def decode_metar():
#    """
#    My Own METAR decode method...
#    """
#    pass


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
