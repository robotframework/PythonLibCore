import argparse

from robot import run_cli

parser = argparse.ArgumentParser("Runner for examples")
parser.add_argument("type", help="Which example is run.")
args = parser.parse_args()
if args.type not in ["static", "dynamic"]:
    raise ValueError("Invalid value for library type.")
run_cli([
    "--pythonpath",
    args.type,
    args.type
])
