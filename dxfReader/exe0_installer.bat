@echo off
setlocal

REM Define the repository and folder name
set REPO_URL=https://github.com/ltsai323/minigantry_softwares.git
set FOLDER_NAME=minigantry_softwares
REM Define required Python modules
set MODULES=ezdxf numpy matplotlib

REM Check if Git is installed
echo Checking for Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Please download it from https://git-scm.com/downloads.
    pause && exit /b
)

REM Check if Python is installed
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please download it from the Microsoft Store or https://www.python.org/downloads.
    pause && exit /b
)


REM Check if required Python modules are installed
for %%M in (%MODULES%) do (
    echo Checking for Python module "%%M"...
    python -c "import %%M" 2>nul
    if %errorlevel% neq 0 (
        echo Python module "%%M" is not installed. Installing with pip...
        pip install %%M
        if %errorlevel% neq 0 (
            echo Failed to install Python module "%%M". Please install it manually.
            pause && exit /b
        )
    )
)

For /f "tokens=1-4 delims=/:. " %%a in ("%DATE%") do (
    SET _year=%%a
    SET _mon=%%b
    SET _day=%%c
    SET _weekday=%%d
	SET mytime=%%b-%%c-%%a
)

REM Check if folder already exists
if exist "%FOLDER_NAME%" (

  echo The folder "%FOLDER_NAME%" already exists.
  echo Do you want to rename it to %FOLDER_NAME%_%mytime% and continue? (Y/N);
  set /p USER_CONFIRM=
	
    if /i "%USER_CONFIRM%"=="Y" (
        set "NEW_FOLDER=%FOLDER_NAME%_%mytime%"
        echo Renaming folder to "%NEW_FOLDER%"...
        ren "%FOLDER_NAME%" "%NEW_FOLDER%"
    ) else (
        echo Operation cancelled by user.
        pause
        exit /b
    )
)

REM Clone the repository
echo Cloning repository "%REPO_URL%"...
git clone %REPO_URL%
if %errorlevel% neq 0 (
    echo Failed to clone the repository. Please check the URL or your internet connection.
    pause && exit /b
)

echo Repository cloned successfully.
pause
endlocal
