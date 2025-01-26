from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    pseudocode = request.json.get('pseudocode')
    python_file = compile_pseudocode_to_python(pseudocode)
    result = subprocess.run(['python3', python_file], capture_output=True, text=True)
    return jsonify({'output': result.stdout, 'error': result.stderr})

def compile_pseudocode_to_python(pseudocode):
    psc_file = 'temp.psc'
    python_file = 'temp.py'
    
    # Save pseudocode to a .psc file
    with open(psc_file, 'w') as file:
        file.write(pseudocode)
    
    # Run your existing compiler to generate a Python file
    # Assuming your compiler is a Python script named 'compiler.py'
    subprocess.run(['python3', 'compiler.py', psc_file, python_file], check=True)
    
    return python_file

if __name__ == '__main__':
    app.run(debug=True)
