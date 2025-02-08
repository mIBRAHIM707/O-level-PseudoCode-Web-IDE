document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#pseudocode-form button').addEventListener('click', async function() {
        const pseudocode = document.getElementById('pseudocode').value;
        const inputData = document.getElementById('input-data').value; // Get input data
        const response = await fetch('/compile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ pseudocode, input_data: inputData }) // Send input data
        });
        const result = await response.json();
        console.log("Received result:", result);
        console.log("Result output:", result.output); // Add this line
        console.log("Result error:", result.error);   // Add this line
        document.getElementById('output').textContent = result.output || result.error;
    });
});