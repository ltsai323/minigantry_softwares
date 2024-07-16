# List of Python modules to check and install
$modules = @("pyyaml", "pyserial", "pyautogui", "pywin32")

# Function to check if a module is installed
function Check-ModuleInstalled {
    param (
        [string]$moduleName
    )

    $result = python -m pip show $moduleName
    return $result -ne $null
}

# Function to install a module
function Install-Module {
    param (
        [string]$moduleName
    )

    Write-Host "Installing module: $moduleName"
    python -m pip install $moduleName
}

# Loop through each module and check if it is installed
foreach ($module in $modules) {
    if (-not (Check-ModuleInstalled -moduleName $module)) {
        Install-Module -moduleName $module
    }
    else {
        Write-Host "Module $module is already installed."
    }
}
