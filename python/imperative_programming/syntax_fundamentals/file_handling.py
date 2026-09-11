# Python file detection

import os # operating system

# Retrieve the exact directory of the python script's location
script_dir = os.path.dirname(os.path.abspath(__file__))

# Join the directory with the target file name securely
file_path = os.path.join(script_dir, "test.txt")

if os.path.exists(file_path): # if the file path contains test.txt -> proving file existance
    print(f"\nThis file location ['{file_path}'] exists")

    if os.path.isfile(file_path): # if the file path is a file
        print("\nThis is a file")

    elif os.path.isdir(file_path): # if file path is a directory
        print("\nThat's a directory")
else:
    print(f"\nThat file location ['{file_path}'] doesn't exist")

