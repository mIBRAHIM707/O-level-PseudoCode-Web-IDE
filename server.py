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
    input_data = request.json.get('input_data', '')  # Get input data from request
    app.logger.debug(f"Received pseudocode: {pseudocode}, input: {input_data}")
    
    # Clear the error.log file
    if os.path.exists("error.log"):
        os.remove("error.log")
    
    try:
        python_file = compile_pseudocode_to_python(pseudocode)
        result = subprocess.run(['python3', python_file], input=input_data, capture_output=True, text=True) # Pass input to subprocess
        app.logger.debug(f"Execution result: {result.stdout}, Error: {result.stderr}")
        if result.returncode != 0:
            raise Exception(result.stderr)
        return jsonify({'output': result.stdout, 'error': result.stderr})
    except Exception as e:
        error_message = str(e)
        app.logger.error(f"Exception: {error_message}")
        if "NameError: Variable" in error_message:
            error_message = error_message.split("NameError: ")[1].split("\n")[0]
        return jsonify({'output': '', 'error': error_message})
    except Exception as e:  # Catch any other exceptions
        app.logger.error(f"Unhandled exception: {e}")
        return jsonify({'output': '', 'error': str(e)})  # Return error to client

def compile_pseudocode_to_python(pseudocode):
    psc_file = 'temp.psc'
    python_file = 'generatedCode.py'
    
    # Save pseudocode to a .psc file
    with open(psc_file, 'w') as file:
        file.write(pseudocode)
    
    # Run your existing compiler (main.py) to generate a Python file
    try:
        result = subprocess.run(['python3', 'Compiler/main.py', psc_file, python_file], capture_output=True, text=True, check=True)
        if result.returncode != 0:
            raise Exception(result.stderr)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Compilation error: {e.stderr}")
    
    return python_file

if __name__ == '__main__':
    app.run(debug=True)
