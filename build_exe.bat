@echo off
REM Build Link Guard EXE using PyInstaller (Windows)
SETLOCAL
echo Installing/updating pyinstaller...
pip install --upgrade pyinstaller
echo Building EXE with PyInstaller...
pyinstaller --onefile --noconsole --add-data "phishing_dataset.csv;." link_guard.py
if exist dist\link_guard.exe (
    echo Moving EXE and dataset to Program Files...
    if not exist "%ProgramFiles%\LinkGuard" mkdir "%ProgramFiles%\LinkGuard"
    move /y dist\link_guard.exe "%ProgramFiles%\LinkGuard\link_guard.exe"
    copy /y phishing_dataset.csv "%ProgramFiles%\LinkGuard\phishing_dataset.csv"
    echo Build complete. EXE and dataset located at "%ProgramFiles%\LinkGuard"
) else (
    echo Build failed. Check pyinstaller output in the console.
)
ENDLOCAL
pause@echo off
REM Build Link Guard EXE using PyInstaller (Windows)
SETLOCAL
echo Installing/updating pyinstaller...
pip install --upgrade pyinstaller
echo Building EXE with PyInstaller...
pyinstaller --onefile --noconsole --add-data "phishing_dataset.csv;." link_guard.py
if exist dist\link_guard.exe (
    echo Moving EXE and dataset to Program Files...
    if not exist "%ProgramFiles%\LinkGuard" mkdir "%ProgramFiles%\LinkGuard"
    move /y dist\link_guard.exe "%ProgramFiles%\LinkGuard\link_guard.exe"
    copy /y phishing_dataset.csv "%ProgramFiles%\LinkGuard\phishing_dataset.csv"
    echo Build complete. EXE and dataset located at "%ProgramFiles%\LinkGuard"
) else (
    echo Build failed. Check pyinstaller output in the console.
)
ENDLOCAL
pause