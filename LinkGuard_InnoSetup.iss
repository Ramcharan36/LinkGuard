; Inno Setup script for Link Guard installer with alternate name
[Setup]
AppName=Link Guard
AppVersion=1.0
DefaultDirName={pf}\LinkGuard
DefaultGroupName=Link Guard
DisableProgramGroupPage=yes
OutputBaseFilename=LinkGuardSetupAlt  ; Updated output filename
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
;SetupIconFile=link_guard.ico  ; Comment out if no .ico file
UninstallDisplayIcon={app}\link_guard.exe

[Files]
Source: "dist\LinkGuard\link_guard.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\LinkGuard\phishing_dataset.csv"; DestDir: "{app}"; Flags: ignoreversion
Source: "whitelist.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "blocklist.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Link Guard"; Filename: "{app}\link_guard.exe"
Name: "{userdesktop}\Link Guard"; Filename: "{app}\link_guard.exe"; Tasks: desktopicon

[Tasks]
Name: "autostart"; Description: "Start Link Guard on Windows startup"; GroupDescription: "Additional Options"; Flags: unchecked

[Registry]
; Auto-start on login (conditional on task)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "LinkGuard"; ValueData: """{app}\link_guard.exe"""; Flags: uninsdeletevalue; Tasks: autostart

; Register as protocol handlers (http/https) with new name
Root: HKCU; Subkey: "Software\Classes\LinkGuardAlt.URL"; ValueType: string; ValueData: "URL:Link Guard Alt Protocol"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\LinkGuardAlt.URL"; ValueName: "URL Protocol"; ValueType: string; ValueData: ""; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\LinkGuardAlt.URL\shell\open\command"; ValueType: string; ValueData: """{app}\link_guard.exe"" ""%1"""; Flags: uninsdeletekey

Root: HKCU; Subkey: "Software\Classes\http"; ValueType: string; ValueData: "URL:http Protocol"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\http"; ValueName: "URL Protocol"; ValueType: string; ValueData: ""; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\http\shell\open\command"; ValueType: string; ValueData: """{app}\link_guard.exe"" ""%1"""; Flags: uninsdeletekey

Root: HKCU; Subkey: "Software\Classes\https"; ValueType: string; ValueData: "URL:https Protocol"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\https"; ValueName: "URL Protocol"; ValueType: string; ValueData: ""; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\https\shell\open\command"; ValueType: string; ValueData: """{app}\link_guard.exe"" ""%1"""; Flags: uninsdeletekey

; Make it appear as browser option in Default Apps with new name
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\LinkGuardAlt"; ValueType: string; ValueData: "Link Guard Alt Browser"; Flags: uninsdeletekeyifempty
Root: HKCU; Subkey: "Software\Clients\StartMenuInternet\LinkGuardAlt\shell\open\command"; ValueType: string; ValueData: """{app}\link_guard.exe"" ""%1"""; Flags: uninsdeletekey

[Run]
Filename: "{app}\link_guard.exe"; Description: "Launch Link Guard"; Flags: nowait postinstall skipifsilent
Filename: "{app}\link_guard.exe"; Parameters: ""; Description: "Register Link Guard (required for first run)"; Flags: runhidden runasoriginaluser

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
Type: dirifempty; Name: "{pf}\LinkGuard"