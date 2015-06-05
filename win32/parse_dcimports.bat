@echo off
cd ..\tools

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<..\PPYTHON_PATH

rem Run the parse_dcimports script
%PPYTHON_PATH% parse_dcimports.py -o ..\otp\distributed\DCClassImports.py ..\astron\dclass\otp.dc ..\astron\dclass\toon.dc

pause
