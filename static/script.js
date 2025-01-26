document.getElementById('pseudocode-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const pseudocode = document.getElementById('pseudocode').value;
    console.log("Sending pseudocode:", pseudocode);
    const response = await fetch('/compile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pseudocode: pseudocode })
    });
    const result = await response.json();
    console.log("Received result:", result);
    document.getElementById('output').textContent = result.output || result.error;
});
