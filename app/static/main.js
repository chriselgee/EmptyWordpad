function pollServer() {
    fetch('poll', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            document.getElementById("dataField").textContent;
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Received data:', data);
        // Process the data here
        if (data.Type == "prompt") {
            console.log("Prompt!");
            document.getElementById("prompt").textContent = data.Prompt;
        }
        // Schedule the next poll
        setTimeout(pollServer, 5000); // Poll every 5 seconds
    })
    .catch(error => {
        console.error('Error during polling:', error);

        // Optionally, schedule a retry here
        setTimeout(pollServer, 1000);
    });
}

