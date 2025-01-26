const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { exec } = require('child_process');
const fs = require('fs');

const app = express();
const port = 5000;

app.use(bodyParser.json());
app.use(cors());

app.post('/compile', (req, res) => {
    const pseudocode = req.body.pseudocode;
    const pythonCode = convertToPython(pseudocode);

    fs.writeFileSync('code.py', pythonCode);

    exec('python code.py', (error, stdout, stderr) => {
        if (error) {
            res.status(500).send(stderr);
        } else {
            res.send(stdout);
        }
    });
});

function convertToPython(pseudocode) {
    // Implement your pseudocode to Python conversion logic here
    return pseudocode; // Placeholder
}

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
