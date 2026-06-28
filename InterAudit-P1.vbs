' InterAudit-P1 launcher — double-click to start the app.
' Runs main.py with pythonw (no console window).
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
folder = fso.GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = folder
sh.Run "pythonw """ & folder & "\main.py""", 0, False
