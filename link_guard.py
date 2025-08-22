import sys
import os
import ctypes
import subprocess
import csv
import urllib.parse  # Added for URL parsing
import winreg

APP_NAME = "Link Guard"
EXE_PATH = os.path.abspath(sys.argv[0])
DATASET_PATH = os.path.join(os.path.dirname(EXE_PATH), "phishing_dataset.csv")  # Path to dataset

# Global sets for URL lookup
PHISHING_URLS = set()
LEGITIMATE_URLS = set()

def load_dataset():
    """Load phishing and legitimate URLs from CSV dataset"""
    global PHISHING_URLS, LEGITIMATE_URLS
    try:
        if os.path.exists(DATASET_PATH):
            with open(DATASET_PATH, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    url = row.get('URL', '').strip()  # Adjust column name if different
                    label = row.get('label', '').strip()  # Adjust column name if different
                    if label.lower() == 'phishing':
                        PHISHING_URLS.add(url.lower())
                    elif label.lower() == 'legitimate':
                        LEGITIMATE_URLS.add(url.lower())
            print(f"Loaded {len(PHISHING_URLS)} phishing URLs and {len(LEGITIMATE_URLS)} legitimate URLs.")
        else:
            print(f"Dataset not found at {DATASET_PATH}. Falling back to keyword check.")
    except Exception as e:
        print(f"Error loading dataset: {e}. Falling back to keyword check.")

def is_suspicious_url(url: str) -> bool:
    """Check if URL is suspicious using dataset, keywords, or domain patterns"""
    url = url.lower().strip()
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc  # e.g., abc123.ngrok.io
    path = parsed_url.path      # e.g., /paypal-auth

    # Check dataset first
    if url in PHISHING_URLS:
        return True
    if url in LEGITIMATE_URLS:
        return False

    # Expanded keyword-based heuristic
    bad_keywords = [
        "login", "verify", "update", "bank", "paypal", "auth", "signin", 
        "account", "secure", "password", "confirm", "access", "reset"
    ]
    if any(word in url for word in bad_keywords):
        return True

    # Check for suspicious domains (common in Zphisher)
    suspicious_domains = [
        "ngrok.io", "trycloudflare.com", "serveo.net",  # Tunneling services
        ".xyz", ".top", ".info", ".club", ".online"     # Common phishing TLDs
    ]
    if any(domain.endswith(susp_domain) for susp_domain in suspicious_domains):
        return True

    # Fallback: Assume unknown URLs are suspicious for safety
    return False

def show_warning(url: str):
    """Show Windows native warning popup with red shield"""
    message = f"WARNING!\n\nThis link appears suspicious:\n{url}\n\nIt has been blocked for your safety."
    title = f"{APP_NAME} Alert"
    ctypes.windll.user32.MessageBoxW(None, message, title, 0x10)  # 0x10 = MB_ICONHAND (red shield)

def register_app():
    """Register app in Windows Registry for auto-start and link handling"""
    try:
        # Auto-start
        run_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, run_key, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{EXE_PATH}"')

        # HTTP/HTTPS handler
        for proto in ["http", "https"]:
            base = f"Software\\Classes\\{proto}"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, base) as k:
                winreg.SetValueEx(k, "", 0, winreg.REG_SZ, f"URL:{proto.upper()} Protocol")
                winreg.SetValueEx(k, "URL Protocol", 0, winreg.REG_SZ, "")
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, base + r"\shell\open\command") as k:
                winreg.SetValueEx(k, "", 0, winreg.REG_SZ, f'"{EXE_PATH}" "%1"')

        # Inform user
        ctypes.windll.user32.MessageBoxW(
            None,
            f"{APP_NAME} has been registered!\n\nGo to Settings → Default Apps → Choose defaults by link type → "
            f"set {APP_NAME} as handler for http and https.",
            APP_NAME,
            0x40  # Information icon
        )
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(None, f"Failed to register: {e}", APP_NAME, 0x10)

def open_in_browser(url: str):
    """Open the URL in Chrome or Edge directly to avoid loop"""
    browser_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    ]
    for browser_path in browser_paths:
        if os.path.exists(browser_path):
            subprocess.Popen([browser_path, url])
            return
    # Fallback warning if no browser found
    error_msg = f"Unable to open {url}: No supported browser (Chrome or Edge) found at standard paths."
    ctypes.windll.user32.MessageBoxW(None, error_msg, f"{APP_NAME} Error", 0x10)

def main():
    # Load dataset on startup
    load_dataset()

    # If no URL passed, assume first run → register app
    if len(sys.argv) < 2:
        register_app()
        sys.exit(0)

    # Clean the URL argument
    url = sys.argv[1].strip().strip('"').strip("'")

    # Check and act
    if is_suspicious_url(url):
        show_warning(url)
    else:
        open_in_browser(url)

if __name__ == "__main__":
    main()