Set ws = CreateObject("WScript.Shell")
ws.CurrentDirectory = "D:\your\path"
ws.Run "powershell.exe -File screemTime.ps1", 0