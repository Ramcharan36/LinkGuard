# uninstall_windows.py - remove registration keys (HKCU)
import winreg, sys

def delete_key_recursive(root, path):
    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as k:
            i = 0
            subkeys = []
            try:
                while True:
                    subkeys.append(winreg.EnumKey(k, i))
                    i += 1
            except OSError:
                pass
        for sub in subkeys:
            delete_key_recursive(root, path + "\\" + sub)
    except Exception:
        pass
    try:
        winreg.DeleteKey(root, path)
    except Exception:
        pass

if __name__ == '__main__':
    delete_key_recursive(winreg.HKEY_CURRENT_USER, r"Software\LinkGuard\Capabilities")
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\RegisteredApplications", 0, winreg.KEY_ALL_ACCESS) as k:
            try:
                winreg.DeleteValue(k, "Link Guard")
            except Exception:
                pass
    except Exception:
        pass
    delete_key_recursive(winreg.HKEY_CURRENT_USER, r"Software\Classes\LinkGuard.URL")
    delete_key_recursive(winreg.HKEY_CURRENT_USER, r"Software\Clients\StartMenuInternet\LinkGuard")
    print("Unregistered Link Guard (HKCU).")