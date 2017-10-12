import pastStats
import schedule
import dataFunctions

from datetime import datetime
import dateutil
from dateutil.parser import parse


schedule = schedule.getSchedule()
teams = {}


def buildTeams():
    for game in schedule['fullgameschedule']['gameentry']:
        homeTeam = game['homeTeam']['abbreviation']
        awayTeam = game['awayTeam']['abbreviation']
        if homeTeam not in teams:
            teams[homeTeam] = {}
        if awayTeam not in teams:
            teams[awayTeam] = {}
        date = game['date'].replace('-', '')
        dateDT = dateutil.parser.parse(date)
        if dateDT < datetime.now():
            gameStats = callGame(homeTeam, awayTeam, date)
            # extractStats(gameStats)
    return teams


def callGame(homeTeam, awayTeam, date):
    endpoint = 'game_boxscore.json'
    payload = {
        'gameid': date + '-' + awayTeam + '-' + homeTeam
    }
    gameStats = dataFunctions.apiGet(endpoint, payload)
    return gameStats


# teams = buildTeams()
# gameDates = schedule.pullGameDates()
# def runAllGames(teams, gameDates):
#     for date in gameDates:
#         for team in teams:
#             gameStats = callGame(


def extractStats(gameStats):
    homeTeam = gameStats['gameboxscore']['game']['homeTeam']['Abbreviation']
    homeTeamStats = gameStats['gameboxscore']['homeTeam']['homeTeamStats']
    awayTeam = gameStats['gameboxscore']['game']['awayTeam']['Abbreviation']
    awayTeamStats = gameStats['gameboxscore']['awayTeam']['awayTeamStats']
    date = gameStats['gameboxscore']['game']['date'].replace('-', '')
    teams[homeTeam][date] = {
        'RYA': awayTeamStats['RushYards']['#text']
        'RTDA': awayTeamStats['RushTD']['#text']
        'PYA': awayTeamStats['PassGrossYards']['#text']
        'PTDA': awayTeamStats['PassTD']['#text']
        'GrossYA': awayTeamStats['OffenseYds']['#text']
    }
    teams[awayTeam][date] = {
        'RYA': homeTeamStats['RushYards']['#text']
        'RTDA': homeTeamStats['RushTD']['#text']
        'PYA': homeTeamStats['PassGrossYards']['#text']
        'PTDA': homeTeamStats['PassTD']['#text']
        'GrossYA': homeTeamStats['OffenseYds']['#text']
    }
