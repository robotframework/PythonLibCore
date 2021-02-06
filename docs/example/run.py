import argparse

from robot import run_cli

parser = argparse.ArgumentParser("Runner for examples")
parser.add_argument("type", help="Which example is run.")
args = parser.parse_args()
if args.type == "static":
    folder = f"01-{args.type}"
elif args.type == "hybrid":
    folder = f"02-{args.type}"
else:
    raise ValueError("Invalid value for library type.")
run_cli([
    "--pythonpath",
    folder,
    folder
])
