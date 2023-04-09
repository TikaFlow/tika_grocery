@echo off
D: & cd D:\your\path
:run
rem 报告自身状态
mqttx.exe pub --config conf\heart.json
timeout /t 7 /nobreak

rem 询问下属状态
mqttx.exe pub --config conf\ask.json
timeout /t 7 /nobreak
goto run
