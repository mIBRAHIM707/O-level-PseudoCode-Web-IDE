from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Add this line
import subprocess
import os
import logging

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    pseudocode = request.json.get('pseudocode')
    input_data = request.json.get('input_data', '')  # Get input data from request
    app.logger.debug(f"Received pseudocode: {pseudocode}, input: {input_data}")
    
    # Clear the error.log file
    if os.path.exists("error.log"):
        os.remove("error.log")
    
    try:
        app.logger.debug("Calling compile_pseudocode_to_python")
        python_file = compile_pseudocode_to_python(pseudocode)
        app.logger.debug(f"Generated python file: {python_file}")
        app.logger.debug("Running subprocess using Popen")
        # Ensure input_data is not empty and ends with a newline
        if input_data == "":
            input_data = "\n"
        if not input_data.endswith("\n"):
            input_data += "\n"
        process = subprocess.Popen(
            ['python3', python_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = process.communicate(input=input_data, timeout=10)
        app.logger.debug(f"Execution result: {out}, Error: {err}")
        if process.returncode != 0:
            raise Exception(err)
        app.logger.debug("Returning jsonify")
        return jsonify({'output': out, 'error': err})
    except subprocess.TimeoutExpired as te:
        app.logger.error(f"Subprocess timed out: {te}")
        return jsonify({'output': '', 'error': 'Execution timed out'})
    except Exception as e:
        error_message = str(e)
        app.logger.error(f"Exception: {error_message}")
        if "NameError: Variable" in error_message:
            error_message = error_message.split("NameError: ")[1].split("\n")[0]
        return jsonify({'output': '', 'error': error_message})

def compile_pseudocode_to_python(pseudocode):
    psc_file = 'temp.psc'
    python_file = 'generatedCode.py'
    
    # Save pseudocode to a .psc file
    app.logger.debug(f"Saving pseudocode to {psc_file}")
    with open(psc_file, 'w') as file:
        file.write(pseudocode)
    
    # Run your existing compiler (main.py) to generate a Python file
    try:
        app.logger.debug(f"Running compiler: python3 Compiler/main.py {psc_file} {python_file}")
        result = subprocess.run(['python3', 'Compiler/main.py', psc_file, python_file], capture_output=True, text=True, check=True)
        app.logger.debug(f"Compiler stdout: {result.stdout}")
        app.logger.debug(f"Compiler stderr: {result.stderr}")
        if result.returncode != 0:
            raise Exception(result.stderr)
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Compilation error: {e}")
        raise Exception(f"Compilation error: {e.stderr}")
    
    return python_file

if __name__ == '__main__':
    app.run(debug=True)
