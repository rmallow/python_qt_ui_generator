from generate import VERSION_TO_COMMAND

import os
import shutil
import sys

PATH_TO_PYTHON = "PATH_TO_PYTHON"
PATH_TO_DIR = "PATH_TO_DIR"
PATH_TO_ENV = "PATH_TO_ENV"
KWARGS = "KWARGS"


def get_library():
    """Get the python library that they are using"""
    print("What python qt library are you using?")
    ver_list = list(VERSION_TO_COMMAND.keys())
    for number, version in enumerate(ver_list):
        print(f"{number+1}. {version}")

    while not (
        (val := input(f"Enter a number 1 - {len(ver_list)}: ")).isnumeric()
        and int(val) > 0
        and int(val) <= len(ver_list)
    ):
        pass
    return list(VERSION_TO_COMMAND.keys())[int(val) - 1]


def get_path():
    """Get the path to the .ui files to generate on"""
    while not (
        (
            path := input(
                "Enter absolute directory path of qt .ui files to auto generate on: "
            )
        )
        and os.path.abspath(path)
        and os.path.isdir(path)
    ):
        pass
    return path


def get_env():
    """Get the path to the env bin to call command from (where Qt is)"""
    while not (
        (
            response := input(
                "Where is the Qt library located? Select y to use your current python path otherwise enter a path: "
            )
        )
        and response.lower() == "y"
        or (os.path.abspath(response) and os.path.isdir(response))
    ):
        pass
    return response


def main():
    library = get_library()
    generate_dir_path = get_path()
    env_path = get_env()
    if env_path.lower() == "y":
        env_path = os.path.join(sys.prefix, "bin")
    cwd = os.getcwd()

    """Create the opt directory"""
    optPath = os.path.join(os.path.abspath(os.sep), "opt", "qt_auto_generate")
    os.makedirs(optPath, exist_ok=True)

    """Create the .plist file and put in Launch Agents"""
    shutil.copyfile(
        os.path.join(cwd, "local.qt_auto_generate.plist"),
        os.path.join(cwd, "new_local.qt_auto_generate.plist"),
    )

    with open("new_local.qt_auto_generate.plist", "r") as file:
        plist_data = file.read()

    plist_data = plist_data.replace(PATH_TO_DIR, generate_dir_path)

    with open("new_local.qt_auto_generate.plist", "w") as file:
        file.write(plist_data)

    launch_agent_path = os.path.join(
        "~", "Library", "LaunchAgents", "local.qt_auto_generate.plist"
    )
    launch_agent_path = os.path.expanduser(launch_agent_path)
    shutil.move(
        os.path.join(cwd, "new_local.qt_auto_generate.plist"),
        launch_agent_path,
    )

    """Create the run.sh file and put in optPath"""
    shutil.copyfile(os.path.join(cwd, "run.sh"), os.path.join(cwd, "new_run.sh"))

    with open("new_run.sh", "r") as file:
        run_script_data = file.read()

    path_to_python = os.path.join(cwd, "generate.py")
    kwargs = f"-v {library} -m 30"
    replace_mapping = [
        (PATH_TO_PYTHON, path_to_python),
        (PATH_TO_DIR, generate_dir_path),
        (PATH_TO_ENV, env_path),
        (KWARGS, kwargs),
    ]
    for k, v in replace_mapping:
        run_script_data = run_script_data.replace(k, v)

    with open("new_run.sh", "w") as file:
        file.write(run_script_data)

    optRunPath = os.path.join(optPath, "run.sh")
    shutil.move(
        os.path.join(cwd, "new_run.sh"),
        optRunPath,
    )

    """Load the launch agent and set permissions"""
    os.system(f"launchctl load {launch_agent_path}")
    os.system(f"chmod +x {optRunPath}")


if __name__ == "__main__":
    main()
