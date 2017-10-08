// function getAuth(URL, username, password, callback) {
//     var xmlHttp = new XMLHttpRequest();
//     string = username + ':' + password
//     xmlHttp.onreadystatechange = function() {
//         if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
//             callback(xmlHttp.responseText);
//         }
//     }
//     xmlHttp.open('GET', URL, true);
//     xmlHttp.setRequestHeader('Authorization': 'Basic ' + btoa(string));
//     xmlHttp.withCredentials = true;
//     xmlHttp.send();
// }


function get(URL, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            callback(xmlHttp.responseText);
        }
    }
    xmlHttp.open('GET', URL, true);
    xmlHttp.send();
}

// RUN get('http://localhost:8080', function(response) {alert(response)})

//CONLCUSION: For some reason, return isn't working in this callback function. Oh, becuase
// your top function getTestA isn't returning anything... return is just fed to argument.


function getSync(URL, username, password) {
    var xmlHttp = new XMLHttpRequest();
    string = username + ':' + password;
    xmlHttp.open('GET', URL, false);
    xmlHttp.setRequestHeader('Authorization', 'Basic ' + btoa(string));
    xmlHttp.send();
    return xmlHttp.responseText
}
