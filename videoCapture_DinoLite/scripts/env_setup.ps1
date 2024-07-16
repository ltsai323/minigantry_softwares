### this file should be executed at 
###     minigantry_softwares/videoCapture_DinoLite/
$PWD = Get-Location
Write-output "Add Current path to PYTHONPATH '$($PWD.Path)'"
Write-output "$env:PYTHONPATH"

$env:PYTHONPATH = "$($PWD.Path);$env:PYTHONPATH"
