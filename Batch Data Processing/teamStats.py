import pastStats
import schedule
import dataFunctions

from datetime import datetime
import dateutil
from dateutil.parser import parse
from pprint import pprint
import time
import pdb


schedule = schedule.getSchedule()
try:
    teamStats = dataFunctions.importLocalJSON('teamStats.txt')
except:
    teamStats = {}


averages1 = ['RYA', 'RTDA', 'PYA', 'PTDA', 'GrossYA']
# teamFields['averages'].update(averages)


def loopGames():
    for game in schedule['fullgameschedule']['gameentry']:
        while True:
            try:
                homeTeam = game['homeTeam']['Abbreviation']
                awayTeam = game['awayTeam']['Abbreviation']
                date = game['date'].replace('-', '')
                dateDT = dateutil.parser.parse(date)
                addTeamsToDict(homeTeam, awayTeam)
                if dateDT < datetime.now() and date not in teamStats[
                        homeTeam]['games']:
                    print('pulling stats and depositing', homeTeam, awayTeam)
                    gameStats = callGame(homeTeam, awayTeam, date)
                    extractStats(gameStats)  # Opens new key for game date
                break
            except ValueError as e:
                print('error', e)
                print('sleeping at', datetime.now().time())
                pdb.set_trace()
                time.sleep(301)
    return teamStats


def addTeamsToDict(homeTeam, awayTeam):
    if homeTeam not in teamStats:
        teamStats[homeTeam] = {
            'averages': {},
            'games': {}
        }
        for key in averages1:
            teamStats[homeTeam]['averages'][key] = {
                'total': 0,
                'average': 0
            }
    if awayTeam not in teamStats:
        teamStats[awayTeam] = {
            'averages': {},
            'games': {}
        }
        for key in averages1:
            teamStats[awayTeam]['averages'][key] = {
                'total': 0,
                'average': 0
            }


def callGame(homeTeam, awayTeam, date):
    endpoint = 'game_boxscore.json'
    payload = {
        'gameid': date + '-' + awayTeam + '-' + homeTeam
    }
    gameStats = dataFunctions.apiGet(endpoint, payload)
    return gameStats


def extractStats(gameStats):
    homeTeam = gameStats['gameboxscore']['game']['homeTeam']['Abbreviation']
    homeTeamStats = gameStats['gameboxscore']['homeTeam']['homeTeamStats']
    awayTeam = gameStats['gameboxscore']['game']['awayTeam']['Abbreviation']
    awayTeamStats = gameStats['gameboxscore']['awayTeam']['awayTeamStats']
    date = gameStats['gameboxscore']['game']['date'].replace('-', '')
    teamStats[homeTeam]['games'][date] = {
        'RYA': int(awayTeamStats['RushYards']['#text']),
        'RTDA': int(awayTeamStats['RushTD']['#text']),
        'PYA': int(awayTeamStats['PassGrossYards']['#text']),
        'PTDA': int(awayTeamStats['PassTD']['#text']),
        'GrossYA': int(awayTeamStats['OffenseYds']['#text'])
    }
    teamStats[awayTeam]['games'][date] = {
        'RYA': int(homeTeamStats['RushYards']['#text']),
        'RTDA': int(homeTeamStats['RushTD']['#text']),
        'PYA': int(homeTeamStats['PassGrossYards']['#text']),
        'PTDA': int(homeTeamStats['PassTD']['#text']),
        'GrossYA': int(homeTeamStats['OffenseYds']['#text'])
    }


def calculateAverages(teamStats):
    for team in teamStats:
        if team != 'league':
            teamDict = teamStats[team]

            # Zero it from the imported file
            for key in teamDict['averages']:
                teamDict['averages'][key]['average'] = 0
                teamDict['averages'][key]['total'] = 0

            # Go through each game and tabulate averages
            gamesPlayed = len(teamDict['games'])
            for game in teamDict['games']:
                game = teamDict['games'][game]
                for key in game:
                    teamDict['averages'][key]['total'] = \
                        teamDict['averages'][key]['total'] + game[key]
            for key in teamDict['averages']:
                if 'TD' in key:
                    teamDict['averages'][key]['average'] = \
                        round(teamDict['averages'][key]['total']
                              / gamesPlayed, 1)
                else:
                    teamDict['averages'][key]['average'] = \
                        round(teamDict['averages'][key]['total']
                              / gamesPlayed, 0)
    calculateLeagueAverages()
    return teamStats


def calculateLeagueAverages():
    teamStats['league'] = {
        'averages': {}
    }
    for key in averages1:
        teamStats['league']['averages'][key] = {
            'average': 0,
            'total': 0
        }
    for team in teamStats:
        # Calculate totals
        if team != 'league':
            teamAverages = teamStats[team]['averages']
            leagueAverages = teamStats['league']['averages']
            for key in teamAverages:
                stat = teamAverages[key]['average']
                leagueAverages[key]['total'] = \
                    round(leagueAverages[key]['total'], 1) + stat
        # Calculate averages
        for key in leagueAverages:
            leagueAverages[key]['average'] = \
                round(leagueAverages[key]['total']/32, 1)
