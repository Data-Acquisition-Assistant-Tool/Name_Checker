@echo off
echo ================================
echo    Namechecker v1.2
echo    Building executable...
echo ================================

REM 清理之前的构建文件
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del *.spec

echo Cleaning completed...

REM 使用PyInstaller打包
echo Starting PyInstaller build...
pyinstaller --onefile ^
    --windowed ^
    --name "Namechecker_1.2" ^
    --icon=none ^
    --add-data "requirements.txt;." ^
    --hidden-import pandas ^
    --hidden-import openpyxl ^
    --hidden-import pandas.io.excel ^
    --hidden-import pandas.io.parsers ^
    --hidden-import tkinter.ttk ^
    --clean ^
    NameCheck_original.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================
    echo Build completed successfully!
    echo Executable location: dist\Namechecker_1.2.exe
    echo ================================
    echo.
    pause
) else (
    echo.
    echo ================================
    echo Build failed! Please check the error messages above.
    echo ================================
    echo.
    pause
)
