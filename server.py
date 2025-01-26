from flask import Flask, request, jsonify, render_template
import subprocess
import os
import logging

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    pseudocode = request.json.get('pseudocode')
    app.logger.debug(f"Received pseudocode: {pseudocode}")
    try:
        python_file = compile_pseudocode_to_python(pseudocode)
        result = subprocess.run(['python3', python_file], capture_output=True, text=True)
        app.logger.debug(f"Execution result: {result.stdout}, Error: {result.stderr}")
        return jsonify({'output': result.stdout, 'error': result.stderr})
    except Exception as e:
        error_message = str(e)
        app.logger.error(f"Exception: {error_message}")
        if os.path.exists("error.log"):
            with open("error.log", "r") as error_file:
                error_message = error_file.read()
        return jsonify({'output': '', 'error': error_message})

def compile_pseudocode_to_python(pseudocode):
    psc_file = 'temp.psc'
    python_file = 'generatedCode.py'
    
    # Save pseudocode to a .psc file
    with open(psc_file, 'w') as file:
        file.write(pseudocode)
    
    # Run your existing compiler (main.py) to generate a Python file
    subprocess.run(['python3', 'Compiler/main.py', psc_file, python_file], check=True)
    
    return python_file

if __name__ == '__main__':
    app.run(debug=True)
