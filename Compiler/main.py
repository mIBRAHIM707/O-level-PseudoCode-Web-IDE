import sys
import os
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), 'srcFiles'))

import argparse
import Tokenizer as tokenizer
import parser as par
from SemanticAnalyzer import SemanticAnalyzer
from CodeGenerator import CodeGenerator
from Optimizer import Optimizer

def read_pseudocode(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main():
    parser = argparse.ArgumentParser(description="O-Level Pseudocode Compiler")
    parser.add_argument("pseudocode_file", help="Path to the pseudocode (.psc) file")
    parser.add_argument("output_file", help="Path to the output Python (.py) file")
    args = parser.parse_args()

    pseudocode = read_pseudocode(args.pseudocode_file)

    try:
        tokens = tokenizer.tokenize(pseudocode)
        print(f"Tokens: {tokens}")  # Debugging line
        parser = par.Parser(tokens)
        ast = parser.parse_program()
        print(f"AST: {ast}")  # Debugging line

        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

        optimizer = Optimizer()
        optimized_ast = optimizer.optimize(ast)
        print(f"Optimized AST: {optimized_ast}")  # Debugging line

        generator = CodeGenerator()
        generator.generate(optimized_ast)
        target_code = generator.get_code()
        print(f"Generated Code: {target_code}")  # Debugging line

        with open(args.output_file, "w") as code_file:
            code_file.write(target_code)

        # Execute the generated Python code and capture any runtime errors
        result = subprocess.run(['python3', args.output_file], capture_output=True, text=True)
        if result.returncode != 0:
            with open("error.log", "w") as error_file:
                error_file.write(result.stderr)
            raise Exception(result.stderr)

    except SyntaxError:
        with open("error.log", "w") as error_file:
            error_file.write("Syntax error in the pseudocode.")
    except Exception as e:
        with open("error.log", "w") as error_file:
            error_file.write(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
