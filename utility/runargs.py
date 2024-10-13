import argparse

parser = argparse.ArgumentParser(description="Example arguments")

# Remove the -- to make it positional, (no defining it like a var)

# Required argument
parser.add_argument("-alt1","--arg1", type=str, help="First argument", required=True)

# Optional argument (default behavior)
parser.add_argument("-alt2","--arg2", type=str, help="First argument")

# Optional argument with a default value
parser.add_argument("-alt3","--arg3", type=str, help="First argument", default="value")

args = parser.parse_args()

print(f"arg1: {args.arg1}")
print(f"arg2: {args.arg2}")
print(f"arg3: {args.arg3}")