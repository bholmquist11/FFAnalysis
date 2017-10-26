serverURLPlayers = 'playerStats.txt'
serverURLTeams = 'teamStats.txt'
weekList = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6',
            'Week 7', 'Week 8', 'Week 9', 'Week 10', 'Week 11',
            'Week 12', 'Week 13', 'Week 14', 'Week 15', 'Week 16', 'Week 17']


function loadLocalPlayerStats() {
    get(serverURLPlayers, function(response) {
        rawStats = response;
        parsedPlayerStats = JSON.parse(rawStats)
    });
    console.log('loaded')
}


function loadLocalTeamStats() {
    get(serverURLTeams, function(response) {
        teamStats = response;
        parsedTeamStats = JSON.parse(teamStats)
    });
    console.log('loaded')
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
    // displayOpponentStats()
}


function displayHandoff2() {
    nameInputFormId = 'WRInput2';
    var playerName = pullName(nameInputFormId).replace(' ', '-');
    pastStatsTableId = 'WRStatsTable2';
    opponentStatsTableId = 'WROpponentTable2'
    playerNameHeadingId = 'playerName2';
    displayPlayerStats(playerName, pastStatsTableId, playerNameHeadingId);
}


function displayPlayerStats(playerName, pastStatsTableId, playerNameHeadingId) {
    singlePlayerStats = retrieveStats(playerName);
    nameHeadingHTML = document.getElementById(playerNameHeadingId).innerHTML
    nameHeadingHTML = playerName
    table = document.getElementById(pastStatsTableId);
    oldBodyRows = table.childNodes[3];
    emptyBodyRows = document.createElement('tbody')
    table.replaceChild(emptyBodyRows, oldBodyRows)
    numWeeks = Object.keys(singlePlayerStats[0]).length
    for (week in weekList.slice(0, numWeeks+1)) {
        console.log(weekList[week])
        if (weekList[week] in singlePlayerStats[0]) {
            weekStats = singlePlayerStats[0][weekList[week]];
            console.log(weekStats)
            row = emptyBodyRows.insertRow();
            row.insertCell(-1).textContent = weekList[week]
            row.insertCell(-1).textContent = weekStats.Opponent // Need to handle bye weeks
            row.insertCell(-1).textContent = weekStats.Receptions
            row.insertCell(-1).textContent = weekStats.Targets
            row.insertCell(-1).textContent = weekStats.RecYards
            row.insertCell(-1).textContent = weekStats.RecTD
        } else {
            row = emptyBodyRows.insertRow();
            row.insertCell(-1).textContent = 'NULL'
        }
    }
}


function retrieveStats(playerName) {
    var singlePlayerStats = parsedPlayerStats.WR[playerName]
    var team = singlePlayerStats['Team']
    return [singlePlayerStats, team]
}


function displayOpponentStats(nameInputFormId, pastStatsTableId, playerNameHeadingId) {
    retrieveStats(nameInputFormId);  // returns singlePlayerStats
    document.getElementById(playerNameHeadingId).innerHTML = WRName
    table = document.getElementById(pastStatsTableId);
    oldBodyRows = table.childNodes[3];
    emptyBodyRows = document.createElement('tbody')
    table.replaceChild(emptyBodyRows, oldBodyRows)
    numWeeks = Object.keys(singlePlayerStats).length
    for (week in weekList.slice(0, numWeeks)) {
        weekStats = singlePlayerStats[weekList[week]];
        row = emptyBodyRows.insertRow();
        row.insertCell(-1).textContent = weekList[week]
        row.insertCell(-1).textContent = weekStats.Opponent
        row.insertCell(-1).textContent = weekStats.Receptions
        row.insertCell(-1).textContent = weekStats.Targets
        row.insertCell(-1).textContent = weekStats.RecYards
        row.insertCell(-1).textContent = weekStats.RecTD
    }
}

