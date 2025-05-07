@ECHO OFF

SET "inputfile=%~1"
if "%inputfile%" == "" (
   ECHO "You need to drag a step2_sortedPoints.LabCoordinate.txt file for execute further command"
   pause
   exit
)

ECHO input file is : "%inputfile%"
python3.exe checkpoints.py "%inputfile%"
pause

