function updateTable(data) { // update the table based on incoming poll data
    const table = document.getElementById('scoreTable');

    // Clear existing table rows, except the header
    while(table.rows.length > 1) {
        table.deleteRow(1);
    }

    // Iterate through each player and add a row for each
    data.forEach(player => {
        const row = table.insertRow(); // Create a new row at the end
        // Create a cell for each data point and append it to the row
        const nameCell = row.insertCell();
        const scoreCell = row.insertCell();
        const promptCell = row.insertCell();
        // Assign the text values for each cell
        nameCell.textContent = player.Name;
        scoreCell.textContent = player.Score;
        promptCell.textContent = player.Prompt;
    });
}

function pollServer(type = "Status", message = "Status") {
    const payload = {
        Type: type,
        Message: message
    };
    fetch('poll', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            payload
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Received data:', data);
        // Process the data here
        switch (data.Type) {
            case "Prompt": // get prompt from server
                console.log("Prompt!");
                document.getElementById("prompt").textContent = data.Prompt;
                break;
            case "Received": // ack answer from player
                console.log("Server received answer " + data["Answer"] + " for player " + data["Player"]);
                break;
            case "Update": // update the player table
                console.log("Received board update like " + data["Update"]);
                updateTable(data["Update"]);
                break;
        }
    })
    .catch(error => {
        console.error('Error during polling:', error);
    });
}

function startPoll() {
    pollServer("Start","Start");

    // poll for status ever 1000 ms
    setInterval(() => {
        pollServer("Status", "Status");
    }, 1000);
};

function sendAnswer () {
    let playerResponse = document.getElementById("dataField").value;
    console.log("Sending answer " + playerResponse);
    pollServer("Answer",playerResponse);
}

window.onload = startPoll();
