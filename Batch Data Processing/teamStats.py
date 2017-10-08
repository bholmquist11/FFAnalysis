import pastStats
import schedule

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
    gameStats = pastStats.apiGet(endpoint, payload)
    return gameStats


# teams = buildTeams()
# gameDates = schedule.pullGameDates()
# def runAllGames(teams, gameDates):
#     for date in gameDates:
#         for team in teams:
#             gameStats = callGame(


def extractStats(gameStats):
    homeTeam = gameStats[_____]
    awayTeam = gameStats[_____]
    date = gameStats[date]
    teams[homeTeam][date]
