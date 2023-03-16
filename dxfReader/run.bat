@ECHO OFF
ECHO input file is : "%~1"
python3.exe dxfReader.py "%~1" && python3.exe sortedPoint.py output_dxfReader.txt
pause
