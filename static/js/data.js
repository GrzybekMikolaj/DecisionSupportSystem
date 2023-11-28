window.globalVar = 0;

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
            // GET data from first row
            params = csv_arr[0];

            // Identify paramters for algorithm
            

            // Prepare Section 2 content and scroll to section 2
            createWeightsForm(params);
            scrollToSection('section2');
        
        }
    }
}

function mergeData(){
    var inputCount = document.getElementById('weightsForm').getElementsByTagName('input').length;
    // console.log(inputCount);
    wght_str = 'weight';
    weightsArr = [];
    for (var i = 0; i < inputCount; i++) {
        str = wght_str.concat('', i);
        // console.log(str);
        var temp_data = document.getElementById(str).value;
        weightsArr.push(temp_data);
    }
    weightsArr.unshift('');
    weightsArr.unshift('Weights');
    // console.log(weightsArr);
    // console.log(window.globalVar);
    window.globalVar.push(weightsArr);
    dataToSend = window.globalVar;
    // console.log(window.globalVar);
    postCsvData(dataToSend);
}

// JavaScript function to handle post request with selected data
function postCsvData(data) {
  
    // Parse data to JSON
    console.log(data);

    // Usunięcie pierwszego wiersza, który zawiera nagłówki kolumn
    const headers = data.shift();

    // Przygotowanie obiektu na podstawie pozostałych wierszy
    const dataObject = {};
    data.forEach(row => {
    const id = row[0];
    const rowData = {};
    headers.slice(1).forEach((header, index) => {
        rowData[header.trim()] = isNaN(row[index + 1]) ? row[index + 1].trim() : parseFloat(row[index + 1].trim());
    });
    dataObject[id] = rowData;
    });

    // Dodanie "weights" do obiektu
    const weightsRow = data.pop();
    const weightsData = {};
    headers.slice(1).forEach((header, index) => {
    weightsData[header.trim()] = isNaN(weightsRow[index + 1]) ? weightsRow[index + 1].trim() : parseFloat(weightsRow[index + 1].trim());
    });
    dataObject['weights'] = weightsData;

    // Konwersja obiektu do JSON
    const json_data = JSON.stringify(dataObject, null, 2);


    json_data = JSON.stringify(data)
    console.log(json_data);

    // Tworzymy nowy obiekt Blob z danymi JSON
    var blob = new Blob([json_data], { type: 'application/json' });

    // Tworzymy link do pobrania pliku
    var link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);

    // Ustawiamy nazwę pliku do pobrania
    link.download = 'dane.json';

    // Dodajemy link do struktury DOM, aby uruchomić proces pobierania
    document.body.appendChild(link);

    // Symulujemy kliknięcie w link, aby uruchomić pobieranie
    link.click();

    // Usuwamy link z DOM
    document.body.removeChild(link);


    // // Fetch API to send a POST request
    // fetch('/algoEnd', {
    //     method: 'POST',
    //     body: json_data,
    //     headers: {
    //         "Content-type": "application/json; charset=UTF-8"}
    // })
    // .then(response => response.json())
    // .then(data => {
    //     console.log('Success:', data);
    // })
    // .catch((error) => {
    //     console.error('Error:', error);
    // });
}

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


