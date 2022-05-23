import os
import time
import argparse

VERSION_TO_COMMAND = {
    "pyside": "pyside-uic",
    "pyside2": "pyside2-uic",
    "pyqt": "pyuic",
    "pyqt5": "pyuic5",
}


def main():
    """Setup Arg Parser"""
    parser = argparse.ArgumentParser(
        description='Generates python code from .ui files in a directory. Appends "ui_" to python code file name'
    )
    parser.add_argument(
        "-e",
        "--env",
        nargs="?",
        const=1,
        default="",
        help="The path to the environment bin to call the command from",
    )
    parser.add_argument(
        "-p",
        "--path",
        nargs="?",
        const=1,
        default=None,
        help="The path to generate the python code from",
    )
    parser.add_argument(
        "-v",
        "--version",
        nargs="?",
        const="pyside2",
        default="pyside2",
        help="Python Qt Library Version for determining command",
    )
    parser.add_argument(
        "-m",
        "--modified",
        nargs="?",
        const=30,
        default=30,
        help="Flag for checking if a .ui file has been modified in the last X seconds before running",
    )
    args = parser.parse_args()
    command = None
    path = None

    if args.version.lower() in VERSION_TO_COMMAND:
        command = VERSION_TO_COMMAND[args.version.lower()]
    else:
        print(
            "Invalid version provided. Choose from: "
            + " ".join(VERSION_TO_COMMAND.keys())
        )
        return

    if args.path is None:
        path = os.getcwd()
    else:
        path = args.path

    if os.path.isdir(path):
        os.chdir(path)
    else:
        print("Not a valid directory path")

    """Get list of ui files and if necessary check if one was modified"""
    ui_files = []
    runCommands = args.modified is None
    for file in os.listdir(os.getcwd()):
        if file.endswith(".ui"):
            ui_files.append(file)
            # if the modified flag is set
            # and we haven't already found a file that has been modified recently
            if args.modified is not None and not runCommands:
                runCommands = time.time() - os.path.getmtime(path) < int(args.modified)

    print(runCommands)
    """Generate python code from files in path"""
    if runCommands:
        for file in ui_files:
            os.system(f"{args.env}/{command} {file} -o ui_{file[:-3]}.py")


if __name__ == "__main__":
    main()
