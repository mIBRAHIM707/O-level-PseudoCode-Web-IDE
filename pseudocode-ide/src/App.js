import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [pseudocode, setPseudocode] = useState('');
    const [output, setOutput] = useState('');

    const handleRun = async () => {
        try {
            const response = await axios.post('http://localhost:5000/compile', { pseudocode });
            setOutput(response.data);
        } catch (error) {
            setOutput(error.response.data);
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
            <button onClick={handleRun}>Run</button>
            <pre>{output}</pre>
        </div>
    );
}

export default App;
