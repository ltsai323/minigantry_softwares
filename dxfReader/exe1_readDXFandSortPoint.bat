@ECHO OFF

SET "filename=%~1"

:: Call PowerShell to show OpenFileDialog if filename not dragged
if "%filename%" == "" (
  set "script_dir=%~dp0"

  for /f "usebackq delims=" %%f in (`powershell -nologo -command "Add-Type -AssemblyName System.Windows.Forms; $ofd = New-Object System.Windows.Forms.OpenFileDialog; $ofd.InitialDirectory = '%script_dir%'; $ofd.Title = 'Select a hexaboard DXF file'; $ofd.Filter = 'DXF Files (*.dxf)|*.dxf|All files (*.*)|*.*'; if ($ofd.ShowDialog() -eq 'OK') { $ofd.FileName }"`) do (
    set "filename=%%f"
  )
)

ECHO input file is : "%filename%"
python3.exe .\python\dxfReader.py "%filename%" && python3.exe .\python\sortedPoint.py step1_dxfReader.txt 0
pause
