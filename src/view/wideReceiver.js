serverURL = 'playerStats.txt'
weekList = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6',
            'Week 7', 'Week 8', 'Week 9', 'Week 10', 'Week 11',
            'Week 12', 'Week 13', 'Week 14', 'Week 15', 'Week 16', 'Week 17']

function buttonListener1() {
    submitButton1 = document.getElementById('WRSubmit1');
    submitButton1.addEventListener('click', displayHandoff1)
}


function buttonListener2() {
    submitButton2 = document.getElementById('WRSubmit2');
    submitButton2.addEventListener('click', displayHandoff2)
}


function loadLocalStats() {
    get(serverURL, function(response) {
        rawStats = response;
        parsedStats = JSON.parse(rawStats)
    });
    console.log('loaded')
}


function displayHandoff1() {
    formId = 'WRInput1';
    tableId = 'WRStatsTable1';
    playerId = 'playerName1';
    console.log
    displayStats(formId, tableId, playerId)
}


function displayHandoff2() {
    formId = 'WRInput2';
    tableId = 'WRStatsTable2';
    playerId = 'playerName2';
    displayStats(formId, tableId, playerId)
}


function displayStats(formId, tableId, playerId) {
    retrieveStats(formId);  // returns singlePlayerStats
    document.getElementById(playerId).innerHTML = WRName
    table = document.getElementById(tableId);
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


function retrieveStats(formId) {
    WRName = pullName(formId);
    WRName = WRName.replace(' ', '-');
    singlePlayerStats = parsedStats.WR[WRName]
}


function pullName(formId) {
    input = document.forms[formId].WRInputBox;
    WRName = input.value;
    return WRName
}


