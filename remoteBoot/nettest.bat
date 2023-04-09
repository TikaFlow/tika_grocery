@echo off
:nettest
ping -n 1 aliyun.com >nul
if errorlevel 1 (
	timeout /t 2 /nobreak
	goto nettest
	)