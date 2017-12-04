# IMPORT / EXPORT DATA
# Imports the most recent full data set from local
import json
import requests
import os
season = '2017-2018-regular'


def importLocalJSON(fileName):
    with open(fileName) as infile:
        localStats = json.load(infile)
    return localStats


def exportLocalJSON(stats, fileName):
    os.chdir(
        'C:/Users/Ben/Google Drive/The Endeavors/Coding/GitHub/FFAnalysis')
    with open(fileName, 'w') as outfile:
        json.dump(stats, outfile)


def apiGet(endpoint, payload={}):
    print('api get', endpoint)
    url = 'https://www.mysportsfeeds.com/api/feed/pull/nfl/' + season \
        + '/' + endpoint
    auth = ('bholmquist11', 'yani991b')
    response = requests.get(url, auth=auth, params=payload).json()
    return response