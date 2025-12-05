@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Standard build for NameChecker 1.5
cd /d %~dp0\..

echo ========================================
echo    NameChecker v1.5 build
echo ========================================

echo Cleaning old build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for %%F in (*.spec) do del /q "%%F"

echo Building executable...
set ICON_PATH=namechecker.ico
if exist assets\icons\namechecker.ico set ICON_PATH=assets\icons\namechecker.ico

py -m PyInstaller ^
  --onefile ^
  --windowed ^
  --name NameChecker_1.5 ^
  --icon "!ICON_PATH!" ^
  --add-data "!ICON_PATH!;." ^
  --hidden-import pandas ^
  --hidden-import numpy ^
  --hidden-import openpyxl ^
  --hidden-import pandas.io.excel ^
  --hidden-import pandas.io.formats.excel ^
  --hidden-import pandas.io.parsers ^
  --hidden-import et_xmlfile ^
  --hidden-import pytz ^
  --hidden-import dateutil ^
  --clean ^
  Namecheck.py

if %ERRORLEVEL% NEQ 0 (
  echo Build failed.
  exit /b 1
)

echo Build success: dist\NameChecker_1.5.exe
endlocal
