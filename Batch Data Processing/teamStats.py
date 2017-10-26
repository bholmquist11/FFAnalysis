import pastStats
import schedule
import dataFunctions

from datetime import datetime
import dateutil
from dateutil.parser import parse
from pprint import pprint
import time


schedule = schedule.getSchedule()
try:
    teamStats = dataFunctions.importLocalJSON('teamStats.txt')
except:
    teamStats = {}


averages1 = ['RYA', 'RTDA', 'PYA', 'PTDA', 'GrossYA']
# teamFields['averages'].update(averages)


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


def loopGames():
    for game in schedule['fullgameschedule']['gameentry']:
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
        except ValueError:
            time.sleep(350)

# BROKEN IN LOOP GAMES WHERE YOU ARE PRINGTIN


def callGame(homeTeam, awayTeam, date):
    endpoint = 'game_boxscore.json'
    payload = {
        'gameid': date + '-' + awayTeam + '-' + homeTeam
    }
    gameStats = dataFunctions.apiGet(endpoint, payload)
    return gameStats


# teamStats = buildTeams()
# gameDates = schedule.pullGameDates()
# def runAllGames(teamStats, gameDates):
#     for date in gameDates:
#         for team in teamStats:
#             gameStats = callGame(


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
        team = teamStats[team]
        gamesPlayed = len(team['games'])
        pprint(team)
        for game in team['games']:
            game = team['games'][game]
            for key in game:
                team['averages'][key]['total'] = \
                    team['averages'][key]['total'] + game[key]
        for key in team['averages']:
            team['averages'][key]['average'] = \
                round(team['averages'][key]['total'] / gamesPlayed, 1)
