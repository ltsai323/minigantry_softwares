@ECHO OFF

SET "inputfile=%~1"
if "%inputfile%" == "" (
   ECHO "You need to drag a DXF file for execute further command"
   pause
   exit
)

ECHO input file is : "%inputfile%"
REM python3.exe ..\dxfReader.py "%inputfile%"
python3.exe ..\sortedPoint.py "%inputfile%" 1
pause
