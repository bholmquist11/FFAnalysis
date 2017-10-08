# IMPORT / EXPORT DATA
# Imports the most recent full data set from local
import json
import requests
season = '2017-2018-regular'


def importLocalJSON(fileName):
    with open('playerStats.txt') as infile:
        localPlayerStats = json.load(infile)
    return localPlayerStats


def exportLocalJSON(playerStats):
    with open('playerStats.txt', 'w') as outfile:
        json.dump(playerStats, outfile)


def apiGet(endpoint, payload={}):
    print('api get', endpoint)
    url = 'https://www.mysportsfeeds.com/api/feed/pull/nfl/' + season \
        + '/' + endpoint
    auth = ('bholmquist11', 'yani991b')
    response = requests.get(url, auth=auth, params=payload).json()
    return response