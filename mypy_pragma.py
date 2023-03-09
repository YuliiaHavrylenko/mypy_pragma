import fileinput
import os
import sys

FOLDER_PATH = "/Users/volt/Coding/Projects/mypy_pragma/files/"


def add_mypy(files_to_modify):
    mypy = "# mypy: enable-option"
    for filename in files_to_modify:
        filepath = os.path.join(FOLDER_PATH, filename)
        # flag to track if mypy has been added to the file
        added_mypy = False
        # check if mypy already in file
        with open(filepath) as f:
            if mypy in f.read():
                print(f"Skipping file: {filename}. '# mypy: enable-option' already exists.")
                continue
        # if mypy not in file, add it after top level module comments
        with fileinput.FileInput(filepath, inplace=True) as file:
            for line in file:
                if line.startswith("#"):
                    print(line, end="")
                else:
                    if not added_mypy:
                        print("# mypy: enable-option")
                        added_mypy = True
                    print(line, end="")


def remove_mypy(files_to_modify):
    mypy_line = "# mypy: enable-option"
    for filename in files_to_modify:
        filepath = os.path.join(FOLDER_PATH, filename)
        with fileinput.FileInput(filepath, inplace=True) as file:
            for line in file:
                if mypy_line in line:
                    continue  # skip line if mypy pragma exists
                print(line, end="")


if __name__ == "__main__":
    # Specify folder containing files to modify
    command = sys.argv[1]
    files_to_modify = sys.argv[2:]
    if command == "add":
        add_mypy(files_to_modify)
    elif command == "remove":
        remove_mypy(files_to_modify)
    else:
        print("Invalid command. Please enter either 'add' or 'remove'.")
