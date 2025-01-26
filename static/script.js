document.getElementById('pseudocode-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const pseudocode = document.getElementById('pseudocode').value;
    const response = await fetch('/compile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pseudocode: pseudocode })
    });
    const result = await response.json();
    document.getElementById('output').textContent = result.output || result.error;
});
