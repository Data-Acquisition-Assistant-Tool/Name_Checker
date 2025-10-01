@echo off
chcp 65001 >nul
echo ========================================
echo    Namechecker v1.4 快速打包工具
echo ========================================
echo.

echo 正在清理旧的构建文件...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del *.spec
echo 清理完成！
echo.

echo 开始使用PyInstaller打包...
echo 这可能需要几分钟时间，请耐心等待...
echo.

set ICON_PATH=namechecker.ico
if exist assets\icons\namechecker.ico set ICON_PATH=assets\icons\namechecker.ico

python -m PyInstaller --onefile --windowed --name Namechecker_1.4 --icon "%ICON_PATH%" --add-data "%ICON_PATH%;." --hidden-import pandas --hidden-import numpy --hidden-import openpyxl --hidden-import pandas.io.excel --hidden-import pandas.io.formats.excel --hidden-import pandas.io.parsers --hidden-import et_xmlfile --hidden-import pytz --hidden-import dateutil --clean Namecheck.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✅ 打包成功完成！
    echo ========================================
    echo.
    echo 📁 exe文件位置: dist\Namechecker_1.4.exe
    
    if exist "dist\Namechecker_1.4.exe" (
        for %%A in ("dist\Namechecker_1.4.exe") do (
            set /a "size_mb=%%~zA / 1024 / 1024"
        )
        call echo 📊 文件大小: %%size_mb%% MB
    )
    
    echo.
    echo 🚀 现在可以将 Namechecker_1.4.exe 复制到任何Windows电脑上运行！
    echo 💡 不需要安装Python或任何其他依赖，可以直接双击运行。
    echo.
    echo 是否要打开文件所在目录？ (y/n)
    set /p "choice="
    if /i "%choice%"=="y" explorer dist
    
) else (
    echo.
    echo ========================================
    echo ❌ 打包失败！
    echo ========================================
    echo 请检查上面的错误信息。
    echo.
)

echo.
echo 按任意键关闭...
pause >nul
