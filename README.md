# python_qt_ui_generator
Scripting to automatically generate python files from qt .ui files. Useful for doing it continually so that IDE can autocomplete on ui definitions.

To setup for MAC only, run sudo python setup.py

This will use Mac launch agents to watch for a change in specified folder and automatically run script on that folder if there is a change.

Requires Python Qt library to be installed.

Depending on system, might need to manually load plist by running:
launchctl load ~/Library/LaunchAgents/local.qt_auto_generate.plist

Another issue could be shell not having full disk access. To resolve:
System Preferences > Security & Privacy > Full Disk Access
    - Add sh and bash