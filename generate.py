import os
import sys
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
    parser.add_argument("path", help="The path to generate the python code from")
    parser.add_argument(
        "-v",
        "--version",
        nargs="?",
        const=1,
        default="pyside2",
        help="Python Qt Library Version for determining command",
    )
    args = parser.parse_args()
    command = None
    if args.version.lower() in VERSION_TO_COMMAND:
        command = VERSION_TO_COMMAND[args.version.lower()]
    else:
        print(
            "Invalid version provided. Choose from: "
            + " ".join(VERSION_TO_COMMAND.keys())
        )
        return

    """Generate python code from files in path"""
    path = args.path
    if os.path.isdir(path):
        os.chdir(path)
        for file in os.listdir(os.getcwd()):
            if file.endswith(".ui"):
                os.system(f"{command} {file} -o ui_{file[:-3]}.py")
    else:
        print("Not a valid directory path")


if __name__ == "__main__":
    main()
