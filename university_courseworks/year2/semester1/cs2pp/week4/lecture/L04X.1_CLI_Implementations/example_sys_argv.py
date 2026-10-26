#!/usr/bin/env python3

import sys
import warnings

"""
 For 3.12 implementation
 import os
 _warn_skips = (os.path.dirname(__file__),)
"""


# Initialize default argument values
input_file = None
output_file = "results.txt"
threshold = 0.5

# Extract the arguments, excluding sys.argv[0] (which is the script name)
args = sys.argv[1:]
# Diagnostically
print(f'{args=}')

# Simple manual parsing of sys.argv
i = 0
while i < len(args):
    arg = args[i]

    if not arg.startswith('-'):
        i += 1
        continue

    if arg in ("--help", "-h"):
        print("Usage: python script.py --input <file> [--output <file>] [--threshold <value>]")
        print()
        print("Options:")
        print("  --input <file>       Specify the input file (required).")
        print(f"  --output <file>      Specify the output file (default: {output_file}).")
        print(f"  --threshold <value>  Specify a threshold (default: {threshold}).")
        print("  --help, -h           Show this help message and exit.")
        sys.exit(0)

    elif arg == "--input":
        i += 1
        if i < len(args):
            input_file = args[i]
        else:
            print("Error: --input requires a file argument.")
            sys.exit(1)

    elif arg == "--output":
        i += 1
        if i < len(args):
            output_file = args[i]
        else:
            print("Error: --output requires a file argument.")
            sys.exit(1)

    elif arg == "--threshold":
        i += 1
        if i < len(args):
            try:
                threshold = float(args[i])
            except ValueError:
                print("Error: --threshold requires a numeric value.")
                sys.exit(1)
        else:
            print("Error: --threshold requires a value.")
            sys.exit(1)

    else:
        print(f"Unknown option: {arg}")
        print("Use --help or -h for usage information.")
        sys.exit(1)

    if args[i].startswith('-'):
        warnings.warn(f'The option value pair: {args[i-1:i+1]} is likely malformed', UserWarning)


    i += 1

# Validate required arguments
if input_file is None:
    print("Error: Missing required --input <file> argument.")
    print("Use --help or -h for usage information.")
    sys.exit(1)

# If we reach here, we have valid arguments
print(f"Input file: {input_file}")
print(f"Output file: {output_file}")
print(f"Threshold: {threshold}")

# Here, you'd perform your main logic.
# E.g., read the input file, process data, write output, etc.

