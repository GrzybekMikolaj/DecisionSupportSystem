 // Function to create and fill the table
 function createTable(rows, columns, data) {
    // console.log(rows, columns)
    var container = document.getElementById("table-container");
    var table = document.createElement("table");

    const header_data = ["Pozycja", "Nazwa", "Punkty"];

    // Loop through rows
    for (var i = 0; i < rows; i++) {
        if(i == 0){
            var row = document.createElement("thead");
        }
        else{
            // Create a table row
            if(i == 1){
                var tbody = document.createElement("tbody");
            }
            var row = document.createElement("tr");
        }

        // Loop through columns
        for (var j = 0; j < columns; j++) {
            if (i == 0){ // Fill table header
                var cell = document.createElement("td");
                cell.textContent = header_data[j];
                row.appendChild(cell);
                continue;
            }
            // Create a table cell
            var cell = document.createElement("td");
            // Set the content of the cell (you can replace this with your custom content)
            if (j == 0){
                temp = i;
                cell.textContent = temp.toString();
                row.appendChild(cell);
                continue;
            }
            obj = data[i-1]
            for (var key in obj) {
                if (obj.hasOwnProperty(key)) {
                    var value = obj[key];
                }
            }
            if (j == 1){
                cell.textContent = key.toString();
                row.appendChild(cell);
                continue;
            }
            if (j == 2){
                cell.textContent = parseFloat(value).toFixed(2);
                row.appendChild(cell);
                continue;
            }
        }
        if(i == 0){
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