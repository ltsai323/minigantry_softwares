Push-Location .
cd ..
.\scripts\env_setup.ps1
Pop-Location
python3 windowsAPI.py
Read-Host -Prompt '...'
