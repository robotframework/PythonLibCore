import argparse

from robot import run_cli

parser = argparse.ArgumentParser("Runner for examples")
parser.add_argument("type", help="Which example is run.")
args = parser.parse_args()
if args.type == "hybrid":
    folder = f"02-{args.type}"
else:
    raise ValueError("Invalid value for library type.")
run_cli(["--loglevel", "trace", "--pythonpath", folder, folder])
