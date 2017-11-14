# For processing all things schedules
import dataFunctions
from datetime import datetime, timedelta
import dateutil
from dateutil.parser import parse

startDate = '20170905'
startDateTime = dateutil.parser.parse(startDate)
now = datetime.now()


def getSchedule():
    schedule = dataFunctions.apiGet('full_game_schedule.json')
    return schedule
schedule = getSchedule()


# Takes a date string ('20171008') and links it up to the week of the season
def datesToWeek(date):
    dateTime = dateutil.parser.parse(date)
    for week in weeks:
        if week[0] <= dateTime < week[1]:
            weekName = week[2]
    return weekName


def pullGameDates():
    schedule = getSchedule()
    gameDates = {}  # The dates of every official game - will contain game info
    for game in schedule['fullgameschedule']['gameentry']:
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


def buildWeeks():
    weeks = []
    for i in range(0, 17):
        week = (startDateTime + timedelta(i*7),
                startDateTime + timedelta((i+1)*7),
                'Week ' + str(i+1))
        weeks.append(week)
    return weeks


def weekNamesOnly(weeks):
    weekNames = []
    for week in weeks:
        weekNames.append(week[2])
    return weekNames


def gamesByDateWithOpponents():
    gamesByDateWithOpponents = {}
    for game in schedule['fullgameschedule']['gameentry']:
        date = game['date'].replace('-', '')
        if date not in gamesByDateWithOpponents:
            gamesByDateWithOpponents[date] = {}
        homeTeam = game['homeTeam']['Abbreviation']
        awayTeam = game['awayTeam']['Abbreviation']
        gamesByDateWithOpponents[date].update({
            homeTeam: awayTeam,
            awayTeam: homeTeam
        })
    return gamesByDateWithOpponents


def opponentsByTeam():
    opponentsByTeam = {}
    for date in gamesByDateWithOpponents:
        week = datesToWeek(date)
        for team in gamesByDateWithOpponents[date]:
            if team not in opponentsByTeam:
                opponentsByTeam[team] = {}
            teamsCurrentOpponent = gamesByDateWithOpponents[date][team]
            opponentsByTeam[team][week] = {
                'Opponent': teamsCurrentOpponent,
                'Date': date
            }
    return opponentsByTeam
gameDates = pullGameDates()
weeks = buildWeeks()
weekNames = weekNamesOnly(weeks)
currentWeek = datesToWeek(str(now))
gamesByDateWithOpponents = gamesByDateWithOpponents()
opponentsByTeam = opponentsByTeam()
