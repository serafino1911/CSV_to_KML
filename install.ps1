# SpeComp Installation Script for Windows
# This script checks for Python, installs dependencies, and sets up the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CSV to KML Converter Setup  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if Python is installed
function Test-PythonInstalled {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+\.\d+\.\d+)") {
            return $true
        }
    } catch {
        return $false
    }
    return $false
}

# Function to get Python version
function Get-PythonVersion {
    try {
        $output = python --version 2>&1
        if ($output -match "Python (\d+\.\d+)") {
            return [version]$matches[1]
        }
    } catch {
        return $null
    }
    return $null
}

# Check if Python is installed
Write-Host "Checking for Python installation..." -ForegroundColor Yellow

if (Test-PythonInstalled) {
    $version = Get-PythonVersion
    Write-Host "[OK] Python found: " -ForegroundColor Green -NoNewline
    python --version
    
    # Check if version is 3.7 or higher
    if ($version -lt [version]"3.7") {
        Write-Host "[ERROR] Python version is too old. Python 3.7 or higher is required." -ForegroundColor Red
        Write-Host "Please download and install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Would you like to download Python installer? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    
    if ($response -eq 'Y' -or $response -eq 'y') {
        Write-Host "Opening Python download page..." -ForegroundColor Cyan
        Start-Process "https://www.python.org/downloads/"
        Write-Host ""
        Write-Host "Please:" -ForegroundColor Yellow
        Write-Host "1. Download and install Python 3.7 or higher" -ForegroundColor White
        Write-Host "2. Make sure to check 'Add Python to PATH' during installation" -ForegroundColor White
        Write-Host "3. Run this script again after installation" -ForegroundColor White
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    } else {
        Write-Host "Installation cancelled." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""

# Check if pip is available
Write-Host "Checking for pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "[OK] pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] pip not found. Installing pip..." -ForegroundColor Red
    python -m ensurepip --upgrade
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install pip" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[OK] pip installed successfully" -ForegroundColor Green
}

Write-Host ""

# Create virtual environment
Write-Host "Setting up virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Cyan
} else {
    python -m venv .venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""

# Activate virtual environment and install requirements
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Cyan

# Activate virtual environment
& ".\.venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install requirements
if (Test-Path "requirements.txt") {
    Write-Host "Installing packages from requirements.txt..." -ForegroundColor Cyan
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] All dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to install some dependencies" -ForegroundColor Red
        Write-Host "Please check the error messages above" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "[ERROR] requirements.txt not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Create launcher script
Write-Host "Creating launcher..." -ForegroundColor Yellow

$launcherContent = @'
@echo off
REM CSV to KML Converter Launcher
title   CSV to KML Converter

echo ========================================
echo    CSV to KML Converter
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run install.ps1 first.
    pause
    exit /b 1
)

REM Activate virtual environment and run the program
call .venv\Scripts\activate.bat
python src\tools\GUI.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Program exited with an error.
    pause
)
'@

Set-Content -Path "make_kml.bat" -Value $launcherContent -Encoding ASCII

if (Test-Path "make_kml.bat") {
    Write-Host "[OK] Launcher created: make_kml.bat" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to create launcher" -ForegroundColor Red
}

Write-Host ""


Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!                " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run CSV to KML Converter:" -ForegroundColor Yellow
Write-Host "  - Double-click 'make_kml.bat'" -ForegroundColor White
Write-Host "  - Or run: .\make_kml.bat" -ForegroundColor White
Write-Host ""
Write-Host "To activate virtual environment manually:" -ForegroundColor Yellow
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
