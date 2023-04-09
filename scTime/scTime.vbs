Set ws = CreateObject("WScript.Shell")
ws.CurrentDirectory = "D:\green\tika"
ws.Run "powershell.exe -File screemTime.ps1", 0