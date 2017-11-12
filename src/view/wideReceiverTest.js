serverURLPlayers = 'playerStats.txt'
serverURLTeams = 'teamStats.txt'
serverURLOpponents = 'opponentsByTeam.txt'
weekList = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6',
            'Week 7', 'Week 8', 'Week 9', 'Week 10', 'Week 11',
            'Week 12', 'Week 13', 'Week 14', 'Week 15', 'Week 16', 'Week 17']


function loadLocalPlayerStats() {
    get(serverURLPlayers, function(response) {
        rawStats = response;
        playerStats = JSON.parse(rawStats);
    });
    console.log('loaded playerStats');
}


function loadLocalTeamStats() {
    get(serverURLTeams, function(response) {
        rawStats = response;
        teamStats = JSON.parse(rawStats);
    });
    console.log('loaded teamStats');
}


function loadLocalOpponents() {
    get(serverURLOpponents, function(response) {
        rawStats = response;
        opponentsByTeam = JSON.parse(rawStats);
    });
    console.log('loaded opponenets');
}


function buttonListener1() {
    submitButton1 = document.getElementById('WRSubmit1');
    submitButton1.addEventListener('click', displayHandoff1)
}


function buttonListener2() {
    submitButton2 = document.getElementById('WRSubmit2');
    submitButton2.addEventListener('click', displayHandoff2)
}


function pullName(nameInputFormId) {
    input = document.forms[nameInputFormId].WRInputBox;
    WRName = input.value;
    return WRName
}


function displayHandoff1() {
    nameInputFormId = 'WRInput1';
    var playerName = pullName(nameInputFormId).replace(' ', '-');
    pastStatsTableId = 'WRStatsTable1';
    opponentStatsTableId = 'WROpponentTable1';
    playerNameHeadingId = 'playerName1';
    displayPlayerStats(playerName, pastStatsTableId, playerNameHeadingId);
}


function displayHandoff2() {
    nameInputFormId = 'WRInput2';
    var playerName = pullName(nameInputFormId).replace(' ', '-');
    pastStatsTableId = 'WRStatsTable2';
    opponentStatsTableId = 'WROpponentTable2';
    playerNameHeadingId = 'playerName2';
    displayPlayerStats(playerName, pastStatsTableId, playerNameHeadingId);
}


function displayPlayerStats(playerName, pastStatsTableId, playerNameHeadingId) {
    document.getElementById(playerNameHeadingId).innerHTML = playerName
    table = document.getElementById(pastStatsTableId);
    oldBodyRows = table.childNodes[3];
    emptyBodyRows = document.createElement('tbody')
    table.replaceChild(emptyBodyRows, oldBodyRows)

    var currentWeek = teamStats.league.currentWeek
    var currentWeekIndex = weekList.indexOf(currentWeek)
    var singlePlayerStats = retrieveStats(playerName);
    var playerStats = singlePlayerStats[0];
    var playerTeam = singlePlayerStats[1];
    var teamOpponents = opponentsByTeam[playerTeam]
    var currentWeek = teamStats.league.currentWeek
    var currentWeekIndex = weekList.indexOf(currentWeek)
    var remainingWeeks = weekList.slice(currentWeekIndex, 17)

    for (week in weekList.slice(0, currentWeekIndex)) {
        if (weekList[week] in singlePlayerStats[0]) {
            weekStats = singlePlayerStats[0][weekList[week]];
            row = emptyBodyRows.insertRow();
            row.insertCell(-1).textContent = weekList[week]
            row.insertCell(-1).textContent = weekStats.Opponent
            row.insertCell(-1).textContent = weekStats.Receptions
            row.insertCell(-1).textContent = weekStats.Targets
            row.insertCell(-1).textContent = weekStats.RecYards
            row.insertCell(-1).textContent = weekStats.RecTD
        } else {
            row = emptyBodyRows.insertRow();
            row.insertCell(-1).textContent = 'NULL'
        }
    }

    row = emptyBodyRows.insertRow()
    row.style.fontWeight = 'bold'
    cell = row.insertCell(-1)
    cell.textContent = 'REMAINING SCHEDULE'
    cell.colSpan = '8'
    row = emptyBodyRows.insertRow()
    row.style.fontWeight = 'bold'
    row.insertCell(-1).textContent = 'Week'
    row.insertCell(-1).textContent = 'Opponent'
    row.insertCell(-1).textContent = 'Av. YA'
    row.insertCell(-1).textContent = 'Rank'
    row.insertCell(-1).textContent = 'Av. PYA'
    row.insertCell(-1).textContent = 'Rank'
    row.insertCell(-1).textContent = 'Av. PTDA'
    row.insertCell(-1).textContent = 'Rank'


    // Insert league averages
    row = emptyBodyRows.insertRow();
    row.insertCell(-1).textContent = 'League'
    row.insertCell(-1).textContent = ''
    row.insertCell(-1).textContent = teamStats['league'].averages.GrossYA.average
    row.insertCell(-1).textContent = ''
    row.insertCell(-1).textContent = teamStats['league'].averages.PYA.average
    row.insertCell(-1).textContent = ''
    row.insertCell(-1).textContent = teamStats['league'].averages.PTDA.average
    row.insertCell(-1).textContent = ''
    for (index in remainingWeeks) {
        if (remainingWeeks[index] in teamOpponents)  {
            var weeklyOpponent = teamOpponents[remainingWeeks[index]]['Opponent'];
            row = emptyBodyRows.insertRow();
            row.insertCell(-1).textContent = remainingWeeks[index]
            row.insertCell(-1).textContent = weeklyOpponent
            row.insertCell(-1).textContent = teamStats[weeklyOpponent].averages.GrossYA.average
            row.insertCell(-1).textContent = teamStats[weeklyOpponent].averages.GrossYA.rank
            row.insertCell(-1).textContent = teamStats[weeklyOpponent].averages.PYA.average
            row.insertCell(-1).textContent = teamStats[weeklyOpponent].averages.PYA.rank
            row.insertCell(-1).textContent = teamStats[weeklyOpponent].averages.PTDA.average
            row.insertCell(-1).textContent = teamStats[weeklyOpponent].averages.PTDA.rank
        } else {
            row = emptyBodyRows.insertRow();
            row.insertCell(-1).textContent = 'BYE'
        }
    }
}


function retrieveStats(playerName) {
    var singlePlayerStats = playerStats.WR[playerName]
    var team = singlePlayerStats['Team']
    return [singlePlayerStats, team]
}

