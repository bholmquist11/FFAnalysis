import requests
import datetime
from datetime import datetime
import dateutil
from dateutil.parser import parse
import math
import json
from pprint import pprint
from datetime import datetime, timedelta
import time
import schedule
import dataFunctions


# INPUTS
season = '2017-2018-regular'
startYear = 2017
startMonth = 9
startDay = 8
startDate = '20170907'
now = datetime.now()
try:
    playerStats = dataFunctions.importLocalJSON('playerStats.txt')
except:
    playerStats = {
        'WR': {},
        'RB': {}
    }

# Category names must match tag names from mySportsFeeds playerStats output
weeklyCategories = {
    'Targets': 0,
    'RecYards': 0,
    'RecTD': 0,
    'RushYards': 0,
    'RushAttempts': 0,
    'RushAverage': 0,
    'RushTD': 0,
    'Receptions': 0
}


def getRoster(positionAbbrev=''):
    payload = {
        'position': positionAbbrev
    }
    endpoint = 'roster_players.json'
    positionRoster = dataFunctions.apiGet(endpoint, payload)
    return positionRoster


def getNamesFromRoster(positionAbbrev=''):
    roster = getRoster(positionAbbrev)
    playerNames = []
    for player in roster['rosterplayers']['playerentry']:
        try:
            name = player['player']['FirstName'] + '-' + player[
                'player']['LastName']
            name = name.replace('.', '')
            team = player['team']['Abbreviation']
            playerNames.append([name, team])
        except KeyError:
            pass
    return playerNames


def pullGameDates():
    yearSchedule = schedule.schedule
    global gameDates
    gameDates = {}
    for game in yearSchedule['fullgameschedule']['gameentry']:
        date = game['date']
        datePlain = date.replace('-', '')
        dateDT = dateutil.parser.parse(datePlain)
        awayTeam = game['awayTeam']['Abbreviation']
        homeTeam = game['homeTeam']['Abbreviation']
        # dates dictionary will have keys for each date. Each date contains
        # dictionaries per game played on that date plus unsorted abbrev of
        # teams who played (used to determine when to API call for players)
        if datePlain in gameDates and dateDT < now:
            gameDates[datePlain].append(game)
            gameDates[datePlain].append(awayTeam)
            gameDates[datePlain].append(homeTeam)
        elif dateDT < now:
            gameDates[datePlain] = [game]
            gameDates[datePlain].append(awayTeam)
            gameDates[datePlain].append(homeTeam)
        else:
            pass
    return gameDates
gameDates = pullGameDates()


def getWeeklyPlayerStats(date, playerName='', stats=[
        'Rec,Yds,TD,Tgt,Att,Avg']):
    payload = {
        'player': playerName,
        'fordate': date,
        'playerstats': stats
    }
    weeklyPlayerStats = dataFunctions.apiGet(
        'daily_player_stats.json', payload)
    return weeklyPlayerStats, date


def reducedWeeklyStats(date, playerName, team):
    week = schedule.datesToWeek(date)
    try:
        weekStats, date = getWeeklyPlayerStats(date, playerName)
        weekStats = weekStats[
            'dailyplayerstats']['playerstatsentry'][0]['stats']
        weekStatsReduced = {}
        # Pull stat for each category, build dictionary off it
        for category in weeklyCategories:
            stat = weekStats[category]['#text']
            weekStatsReduced[category] = stat
        weekStatsReduced['Game Date'] = date
        weekStatsReduced['Opponent'] = schedule.gamesByDateWithOpponents[
            date][team]
        playerStats['WR'][playerName][week] = weekStatsReduced
    except KeyError:
        playerStats['WR'][playerName][week] = 'No stats this week'


def getReceiverStats(playerName, team, gameDates):
    if playerName not in playerStats['WR']:
        print(playerName, 'not found in playerStats')
        playerStats['WR'][playerName] = {'Team': team}
    for date in gameDates:
        week = schedule.datesToWeek(date)
        # If they played on this date and we don't have it in local playerStats
        if team in gameDates[date]:
            if week not in playerStats['WR'][playerName]:
                print(week, 'not found in', playerName, 'stats')
                reducedWeeklyStats(date, playerName, team)


def getAllReceiverStats(playerSetStart, playerSetEnd):
    playerNames = getNamesFromRoster('WR')
    for player in playerNames[playerSetStart:playerSetEnd]:
        try:
            name = player[0]
            team = player[1]
            getReceiverStats(name, team, gameDates)
        except ValueError:
            time.sleep(350)


def getRunningBackStats(playerName, team, gameDates):
    if playerName not in playerStats['RB']:
        print(playerName, 'not found in playerStats')
        playerStats['RB'][playerName] = {}
    for date in gameDates:
        week = schedule.datesToWeek(date)
        # If they played on this date and we don't have it in local playerStats
        if team in gameDates[date]:
            if week not in playerStats['RB'][playerName]:
                print(week, 'not found in', playerName, 'stats')
                reducedWeeklyStats(date, playerName, team)


def getAllRunningBackStats(playerSetStart, playerSetEnd):
    playerNames = getNamesFromRoster('RB')
    for player in playerNames[playerSetStart:playerSetEnd]:
        name = player[0]
        team = player[1]
        getReceiverStats(name, team, gameDates)
