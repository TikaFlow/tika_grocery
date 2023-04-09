@echo off & setlocal enabledelayedexpansion
D: & cd D:\your\path
:monitor
if not exist powerInfo.log echo powerInfo: nothing >powerInfo.log
for /f "tokens=5" %%i in ('type powerInfo.log') do (set lastLine=%%~i)

if "%lastLine%" == "your-power-off-command" (mqttx.exe pub --config
shutdown /s /t 60)

timeout /t 5 /nobreak
goto monitor