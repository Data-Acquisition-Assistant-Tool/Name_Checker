@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 标准化构建 Namechecker 1.41
cd /d %~dp0\..

echo ========================================
echo    Namechecker v1.41 标准化打包
echo ========================================

echo 清理旧产物...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for %%F in (*.spec) do del /q "%%F"

echo 开始打包...
set ICON_PATH=namechecker.ico
if exist assets\icons\namechecker.ico set ICON_PATH=assets\icons\namechecker.ico

python -m PyInstaller ^
  --onefile ^
  --windowed ^
  --name Namechecker_V1.41 ^
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
  echo 打包失败！
  exit /b 1
)

echo 打包成功：dist\Namechecker_V1.41.exe
endlocal

@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 标准化构建 Namechecker 1.4
cd /d %~dp0\..

echo ========================================
echo    Namechecker v1.4 标准化打包
echo ========================================

echo 清理旧产物...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for %%F in (*.spec) do del /q "%%F"

echo 开始打包...
set ICON_PATH=namechecker.ico
if exist assets\icons\namechecker.ico set ICON_PATH=assets\icons\namechecker.ico

python -m PyInstaller ^
  --onefile ^
  --windowed ^
  --name Namechecker_1.4 ^
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
  echo 打包失败！
  exit /b 1
)

echo 打包成功：dist\Namechecker_1.4.exe
endlocal
