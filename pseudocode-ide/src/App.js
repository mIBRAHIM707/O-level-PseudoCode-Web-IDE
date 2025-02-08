import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [pseudocode, setPseudocode] = useState('');
    const [output, setOutput] = useState('');
    const [inputData, setInputData] = useState('');

    const handleRun = async () => {
        try {
            const response = await axios.post('http://localhost:5000/compile', { pseudocode, input_data: inputData });
            console.log("Response data:", response.data); // Add this line
            setOutput(response.data.output || response.data.error);
        } catch (error) {
            setOutput(error.response.data.error);
        }
    };

    return (
        <div className="App">
            <h1>Pseudocode IDE</h1>
            <textarea
                value={pseudocode}
                onChange={(e) => setPseudocode(e.target.value)}
                placeholder="Write your pseudocode here..."
            />
            <input
                type="text"
                value={inputData}
                onChange={(e) => setInputData(e.target.value)}
                placeholder="Enter input for READ statements"
            />
            <button onClick={handleRun}>Run</button>
            <pre>{output}</pre>
        </div>
    );
}

export default App;
