# SET UP SEASON STRUCTURE
# Import schedule from MySportsAPI
# Create data structures for teams, create list of teams
# Ben Holmquist, 3-17-17
# ================================================

url = 'https://www.mysportsfeeds.com/api/feed/pull/nfl/' \
    + season + '/full_game_schedule.json'
auth = ('bholmquist11', 'yani991b')
seasonSchedule = requests.get(url, auth=auth).json()

url = 'https://www.mysportsfeeds.com/api/feed/pull/nfl/' \
    + season + '/active_players.json'
auth = ('bholmquist11', 'yani991b')
activePlayers = requests.get(url, auth=auth).json()[
    'activeplayers']['playerentry']

# TEAMS

teamsList = [
    'DEN', 'CAR', 'GB', 'JAX', 'BUF', 'BAL', 'CHI', 'HOU', 'CLE',
    'PHI', 'TB', 'ATL', 'MIN', 'TEN', 'CIN', 'NYJ', 'OAK', 'NO',
    'SD', 'KC', 'MIA', 'SEA', 'NYG', 'DAL', 'DET', 'IND', 'NE',
    'ARI', 'PIT', 'WAS', 'LA', 'SF'
    ]

global teams
teams = {}
for i in range(len(teamsList)):
    teams[teamsList[i]] = {
        'PYA': 0, 'RYA': 0, 'PTDA': 0, 'RTDA': 0, 'Games Played': 0
    }
leagueAverages = {
    'PYA': 0, 'RYA': 0, 'PTDA': 0, 'RTDA': 0, 'Games Played': 0
}

# Build list of 32 NFL teams; create new dictionary key for each team,
# and initialize their stats PYA RYA RTDA and PTDA to 0. Same for
# league averages.
print('built teams list')

# SCHEDULE

# Build matrix for week 1
schedule = []
for i in range(256):
    schedule.append([0, 0, 0])
scheduleDT = []  # DT indicates datetime format
for i in range(256):
    scheduleDT.append([0, 0, 0])

# Populate matrix with game schedules; away team is in
# [0], home team in [1], date is in [2]
for i in range(256):
    schedule[i][0] = seasonSchedule['fullgameschedule']['gameentry'][i][
        'awayTeam']['Abbreviation']
    schedule[i][1] = seasonSchedule['fullgameschedule']['gameentry'][i][
        'homeTeam']['Abbreviation']
    schedule[i][2] = seasonSchedule['fullgameschedule']['gameentry'][i][
        'date']

# Remove '-' from dates
for i in range(256):
    schedule[i][2] = schedule[i][2].replace('-', '')

# Change format to datetime format for comparison to current date
# Save original schedule for datetime formats
scheduleDT = schedule[:]
for i in range(256):
    scheduleDT[i] = [seasonSchedule['fullgameschedule']['gameentry'][i][
        'awayTeam']['Abbreviation'], seasonSchedule['fullgameschedule'][
        'gameentry'][i]['homeTeam']['Abbreviation']
        ], datetime.strptime(scheduleDT[i][2], '%Y%m%d')
