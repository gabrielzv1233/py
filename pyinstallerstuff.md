# in script stuff
* get executible path (pyinstaller exe or .py) `sys.argv[0]`

# compiling
* basically always use `--oncefile`
* compile without console `pyinstaller app.py --noconsole`
* add an icon `pyinstaller app.py --icon="{filepath}"`
* `--hide-console {minimize-early,hide-early,hide-late,minimize-late}` hide console
* ask for elevation `--uac-admin` to work on remote desktop `--uac-uiaccess`