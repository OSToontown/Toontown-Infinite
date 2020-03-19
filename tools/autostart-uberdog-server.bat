@echo off
cd ..
title Toontown Infinite UberDOG

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PYTHON_PATH=<PYTHON_PATH

rem Define some constants for our UberDOG server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7100
set EVENTLOGGER_IP=127.0.0.1:7198

rem Get the user input:
set BASE_CHANNEL=1000000

:main

%PYTHON_PATH% ^
	-m toontown.uberdog.ServiceStart ^
	--base-channel %BASE_CHANNEL% ^
	--max-channels %MAX_CHANNELS% ^
	--stateserver %STATESERVER% ^
	--astron-ip %ASTRON_IP% ^
	--eventlogger-ip %EVENTLOGGER_IP%
PAUSE
goto main
