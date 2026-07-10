import subprocess

APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "command prompt": "cmd.exe",
    "explorer": "explorer.exe",
}


def open_app(app_name):
    app_name = app_name.lower().strip()

    if app_name in APPS:
        subprocess.Popen(APPS[app_name])
        return True

    return False