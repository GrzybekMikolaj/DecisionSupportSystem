 
 function retrieveData() {
    // Get algorithm parameters from user input in section 2
    // TODO

    // Merge user input with algo parameters into one data (i guess?)
    // TODO

    // POST data to the backend
    postCsvData()
    .then(data => {
        console.log('Data to be used:', data);
        // Once successfully got data from the backend, unwrap it and fit into CSVArray
        // TODO: implement function as described

        // Get Data about Table Size
        // TODO: implement function as described


        // Create the table
        createTable(10, 15);
    })
    .catch(error => {
        // Handle errors from the fetchDataFromEndpoint function
        console.error('Error in fetching data:', error);
    });
 }
 
 // Function to create and fill the table
 function createTable(rows, columns) {
    // Get the container element
    var container = document.getElementById("table-container");
    // Create a table element
    var table = document.createElement("table");

    // Loop through rows
    for (var i = 0; i < rows; i++) {
        if(i == 0){ // Crate a table header
            var row = document.createElement("thead");
        }
        else{
            // Create a table row
            if(i == 1){
                // Create the table body
                var tbody = document.createElement("tbody");
            }
            var row = document.createElement("tr");
        }

        // Loop through columns
        for (var j = 0; j < columns; j++) {
            // Create a table cell
            var cell = document.createElement("td");
            // Set the content of the cell (you can replace this with your custom content)
            cell.textContent = "R " + (i + 1) + ", C " + (j + 1);
            // Append the cell to the row
            row.appendChild(cell);
        }
        if(i == 0){
            // Append the row to the table body
            table.appendChild(row);
        }
        else{
            tbody.appendChild(row);
        }
    }
    // Append the table body to the table
    table.appendChild(tbody);
    // Append the table to the container
    container.appendChild(table);
}
