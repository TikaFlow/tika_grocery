@echo off
D: & cd D:\your\path
:run
rem ��������״̬
mqttx.exe pub --config conf\heart.json
timeout /t 7 /nobreak

rem ѯ������״̬
mqttx.exe pub --config conf\ask.json
timeout /t 7 /nobreak
goto run
