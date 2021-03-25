import argparse
import json
from parse import parse_to_ast
from run import run

def get_args():
    parser = argparse.ArgumentParser(description="A script that streamlines testing out form-based websites. Please see README.md for the details on the input file")
    parser.add_argument("--input", "-i", required=True, help="the file describing the form you want to test. See README.md for details")

    return parser.parse_args()

def main(args):
    with open(args.input) as file:
        raw_json = json.load(file)

    ast = parse_to_ast(raw_json)
    run(ast)

if __name__ == "__main__":
    main(get_args())