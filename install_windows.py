# install_windows.py - register Link Guard in HKCU so it appears in Default Apps
import os, sys, subprocess
EXE_PATH = r"C:\Program Files\LinkGuard\link_guard.exe"  # Verify this path
APP_NAME = "Link Guard"
PROG_ID = "LinkGuardA.URL"
APP_CAP_SUBKEY = r"Software\LinkGuard\Capabilities"
CAP_KEY = r"Software\RegisteredApplications"
CLASSES_ROOT = r"Software\Classes"

def reg_set(root, path, name, value, kind=None):
    try:
        import winreg
        k = winreg.CreateKeyEx(root, path, 0, winreg.KEY_SET_VALUE)
        if kind is None:
            kind = winreg.REG_SZ
        winreg.SetValueEx(k, name, 0, kind, value)
        winreg.CloseKey(k)
    except Exception as e:
        print("Registry write failed:", e)

def create_prog_id():
    cmd = f'"{EXE_PATH}" "%1"'
    reg_set(__import__('winreg').HKEY_CURRENT_USER, f"{CLASSES_ROOT}\\{PROG_ID}", None, APP_NAME)
    reg_set(__import__('winreg').HKEY_CURRENT_USER, f"{CLASSES_ROOT}\\{PROG_ID}", "URL Protocol", "")
    reg_set(__import__('winreg').HKEY_CURRENT_USER, f"{CLASSES_ROOT}\\{PROG_ID}\\DefaultIcon", None, EXE_PATH)
    reg_set(__import__('winreg').HKEY_CURRENT_USER, f"{CLASSES_ROOT}\\{PROG_ID}\\shell\\open\\command", None, cmd)

def create_capabilities():
    reg_set(__import__('winreg').HKEY_CURRENT_USER, APP_CAP_SUBKEY, "ApplicationName", APP_NAME)
    reg_set(__import__('winreg').HKEY_CURRENT_USER, APP_CAP_SUBKEY, "ApplicationDescription", "Checks links for phishing before opening.")
    reg_set(__import__('winreg').HKEY_CURRENT_USER, f"{APP_CAP_SUBKEY}\\URLAssociations", "http", PROG_ID)
    reg_set(__import__('winreg').HKEY_CURRENT_USER, f"{APP_CAP_SUBKEY}\\URLAssociations", "https", PROG_ID)
    reg_set(__import__('winreg').HKEY_CURRENT_USER, CAP_KEY, APP_NAME, APP_CAP_SUBKEY)

if __name__ == '__main__':
    if not os.path.exists(EXE_PATH):
        print("ERROR: EXE not found. Update EXE_PATH in this script and try again.")
        sys.exit(1)
    create_prog_id()
    create_capabilities()
    print("Registered Link Guard. Opening Default Apps settings...")
    subprocess.Popen(["start", "ms-settings:defaultapps"], shell=True)
    sys.exit(0)