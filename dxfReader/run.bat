@ECHO OFF

SET "inputfile=%~1"
if "%inputfile%" == "" (
   ECHO "You need to drag a DXF file for execute further command"
   pause
   exit
)

ECHO input file is : "%inputfile%"
python3.exe dxfReader.py "%inputfile%" && python3.exe sortedPoint.py output_dxfReader.txt
pause
