@echo off
REM Run the sniff.exe file
echo Starting sniff.exe...
start "Sniff Program" "C:\Users\adity\Desktop\final pro\final\test\sniff.exe"

REM Wait for sniff.exe to start before executing the next command
timeout /t 2 >nul

REM Run the Snort command
echo Starting Snort...
start cmd /c "C:\Snort\bin\snort -i 4 -c C:\Snort\etc\snort.conf -A console"

REM Run the exp.py Python script
echo Starting exp.py...
start "Python Script" python "C:\Users\adity\Desktop\final pro\final\test\exp.py"

REM Pause to keep the window open
pause
