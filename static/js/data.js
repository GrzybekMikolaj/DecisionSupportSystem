window.globalVar = 0;
window.globalResult = 0;

function dragOverHandler(event) {
    event.preventDefault();
    event.target.style.border = "2px dashed #aaa";
}

function dropHandler(event) {
    event.preventDefault();
    event.target.style.border = "2px dashed #ccc";

    const files = event.dataTransfer.files;
    handleFiles(files);
}

function handleFiles(files) {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const resultDiv = document.getElementById('result'); // debug only

    if (files.length > 0) {
        var file = files[0];
        const fileName = file.name;
        dropArea.innerHTML = `<p>File ${fileName} selected.</p>`;

        var reader = new FileReader();
        reader.readAsText(file);
        reader.onload = function(event) {
            var csvdata = event.target.result;
            csv_arr = CSVToArray(csvdata, ',');
            window.globalVar = csv_arr;

            // console.log(window.globalVar);            

        }
    }
}

function mergeData(){

    // Sprawdz jaki to algorytm
    var selected_algo = document.getElementById('algorithm').value;

    // Wyciagnij parametry z wybrynaego algorytmu
    if (selected_algo = 'topsis'){
        var params_input = document.querySelectorAll("#form_params > #topsis_params > input");
        var algo_settings = [];

        algo_settings[0] = String(selected_algo);
        
        var i = 1;
        for (const input of params_input){
            algo_settings[i] = input.value;
            i = i+1;
        }
    }
    // TODO: Dopisz brakujące algorytmy 

    window.globalVar.splice(1, 0, algo_settings);
    merged_data = window.globalVar;
    // console.log(merged_data);

    postCsvData(merged_data);
}

 
function postCsvData(input_data) {
    const [header, ...rows] = input_data;
    const jsonObjects = {};
    
    rows.forEach((data) => {
      const key = data[0];
      jsonObjects[key] = {};
    
      header.slice(1).forEach((headerItem, index) => {
        jsonObjects[key][headerItem] = isNaN(data[index + 1]) ? data[index + 1] : parseInt(data[index + 1], 10);
      });
    });

    const jsonString = JSON.stringify(jsonObjects, null, 1);
    // console.log(jsonString);

    // Fetch API to send a POST request
    fetch('http://127.0.0.1:8000/api/endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonString
    })
    .then(resp => resp.json()) 
    .then(data => {
        console.log(data);

        const tableNode = document.getElementById("table-container");
        tableNode.innerHTML = '';
        scrollToSection('section3');
        createTable(7, 3, data);
    })
    .catch(error => {
        console.error(error);
    });
}

// function handleServerResp(data){
//     console.log(data)
//     var rows = 7; // +1 for header
//     var cols = 3;
//     return (rows, cols)
// }

function CSVToArray( strData, strDelimiter ){
    strDelimiter = (strDelimiter || ",");

    var objPattern = new RegExp(
        (
            "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +

            "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +

            "([^\"\\" + strDelimiter + "\\r\\n]*))"
        ),
        "gi"
        );

    var arrData = [[]];
    var arrMatches = null;

    while (arrMatches = objPattern.exec( strData )){
        var strMatchedDelimiter = arrMatches[ 1 ];

        if (
            strMatchedDelimiter.length &&
            (strMatchedDelimiter != strDelimiter)
            ){
            arrData.push( [] );
        }
        if (arrMatches[ 2 ]){
            var strMatchedValue = arrMatches[ 2 ].replace(
                new RegExp( "\"\"", "g" ),
                "\""
                );

        } else {
            var strMatchedValue = arrMatches[ 3 ];

        }
        arrData[ arrData.length - 1 ].push( strMatchedValue );
    }
    return( arrData );
}


function getFormElelemets(formName){
    var elements = document.forms[formName].elements;
    for (i=0; i<elements.length; i++){
    //   console.log(i);
    }
  }