function pollServer(type, message) {
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
        if (data.Type == "Prompt") {
            console.log("Prompt!");
            document.getElementById("prompt").textContent = data.Prompt;
        }
        // Schedule the next poll
        // setTimeout(pollServer, 5000); // Poll every 5 seconds
    })
    .catch(error => {
        console.error('Error during polling:', error);
    });
}

function startPoll() {
    pollServer("Start","Start");
    // Optionally, schedule a retry here
    // setTimeout(pollServer, 1000);
};

function sendAnswer () {
    let playerResponse = document.getElementById("dataField").value;
    console.log("Sending answer " + playerResponse);
    pollServer("Answer",playerResponse);
}

window.onload = startPoll();
