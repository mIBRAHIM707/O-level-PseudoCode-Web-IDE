document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#pseudocode-form button').addEventListener('click', async function() {
        const pseudocode = document.getElementById('pseudocode').value;
        const inputData = document.getElementById('input-data').value; // Get input data
        
        console.log("Sending request to /compile");
        
        const body = JSON.stringify({ pseudocode, input_data: inputData });
        
        try {
            const response = await fetch('/compile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                    // Removed 'Content-Length' header to avoid forbidden header issues
                },
                body: body
            });
            
            console.log("Received response from /compile");
            console.log("Response status:", response.status);
            
            const result = await response.json();
            
            console.log("Parsed JSON result:", result);
            console.log("Result output:", result.output);
            console.log("Result error:", result.error);
            
            document.getElementById('output').textContent = result.output || result.error;
        } catch (error) {
            console.error("Fetch error:", error);
            document.getElementById('output').textContent = "Fetch error: " + error;
        }
    });
});