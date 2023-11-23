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
            // console.log(csv_arr);
            // params_num = csv_arr[0].length - 1;
            // console.log(params_num);
            // resultDiv.innerHTML = csv_arr[0];
            
            // GET data from first row
            // TODO:

            // Identify paramters for algorithm
            // TODO

            // Prepare Section 2 content and scroll to section 2
            // TODO 
        }
    }
}

// JavaScript function to handle post request with selected data
function postCsvData(file) {
    // Get data from web page
    // var data = document.querySelector('#fileCsv').files;
    
    // Parse data to JSON
    console.log(file)
    json_data = JSON.stringify({
                userId: 1,
                title: "User Data",
                completed: false})

    // Fetch API to send a POST request
    fetch('/algoEnd', {
        method: 'POST',
        body: json_data,
        headers: {
            "Content-type": "application/json; charset=UTF-8"}
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
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