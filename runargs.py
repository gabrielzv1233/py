import argparse

parser = argparse.ArgumentParser(description="Example script with optional arguments")

#remove the -- to make it positional, (no defining it like a var)

# Required argument
parser.add_argument("--arg1", type=str, help="First argument", required=True)

# Optional argument (default behavior)
parser.add_argument("--arg2", type=str, help="First argument")

# Optional argument with a default value
parser.add_argument("--arg3", type=str, help="First argument", default="value")

args = parser.parse_args()

print(f"arg1: {args.arg1}")
print(f"arg2: {args.arg2}")