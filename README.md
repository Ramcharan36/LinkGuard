

# Link Guard — Real-time URL Phishing Protection

**Author:** [CHILUMURI. SREE RAM SAI CHARAN]
**Date:** 2025-08-19

## Abstract
This project builds a lightweight Windows desktop application that intercepts clicked HTTP/HTTPS links, checks them against a phishing dataset (e.g., PhiUSIIL Phishing URL Dataset from Kaggle) and local heuristics, opens safe links in Chrome or Edge, and blocks suspicious links with a native warning dialog.

## Installation & Usage
1. Download a phishing dataset (e.g., PhiUSIIL Phishing URL Dataset from Kaggle) and place it as `phishing_dataset.csv` in the project directory.
2. Build `link_guard.exe` using PyInstaller (or use the prebuilt EXE).
3. Run installer (or copy files, including `phishing_dataset.csv`) to `C:\Program Files\LinkGuard`.
4. Run `install_windows.py` to register Link Guard in Default Apps.
5. In Settings → Default apps → Choose defaults by link type → set `http` and `https` to Link Guard.
6. Optionally enable auto-start through the installer or registry.

## Testing
- Test with benign links (e.g., `openai.com`, URLs labeled `legitimate` in the dataset) and suspicious patterns (e.g., URLs labeled `phishing` or containing "login").
- Verify native red-shield popup appears for blocked links and browser does not open.
- Confirm legitimate links open in Chrome or Edge without errors.

## Conclusion
A privacy-first, local-prevention approach using a Kaggle phishing dataset for improved accuracy. Can be extended with on-device ML, signed updates, and enterprise deployment tools.
