import argparse
import sys

# Create the parser
parser = argparse.ArgumentParser(description="Example argparse snippet for demonstration.")

"""
Add the --verbose flag (no value needed; just indicates 'True' if present)
  The `action` keyword argument specifies how the command-line arguments should be handled.
  "store_true" is a special case to store True if the option is present.
"""
parser.add_argument("--verbose", '-v', action="store_true", help="Enable extra debug information.")

"""
In a notebook, we can ---SIMULATE--- command-line arguments by setting sys.argv manually.
Note: sys.argv[0] is typically the script name, so we include a placeholder.
sys.argv = ["demo_script.py", "--verbose"]  # Try removing '--verbose' to see the difference.
"""

# Parse the arguments
args = parser.parse_args()

# Use the parsed arguments
if args.verbose:
    print("Verbose mode is ON. Extra debug info will be printed here...")
else:
    print("Verbose mode is OFF. Minimal output.")


'''
To use this in a more realistic setting,
- transfer the code to a module file.
- remove the manual assignment of sys.argv
- save
- execute: `python module_file.py -h`

''';

