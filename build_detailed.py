#!/usr/bin/env python3
"""
Namechecker - Build Script
This script creates a standalone executable for the file checking tool.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_files():
    """Clean previous build files"""
    print("🧹 Cleaning previous build files...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed: {dir_name}")
    
    # Clean spec files
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"   Removed: {spec_file}")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable with PyInstaller...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single executable file
        '--windowed',                   # No console window (GUI only)
        '--name', 'Namechecker_1.2',  # Output name
        '--clean',                      # Clean cache
        '--noconfirm',                  # Overwrite output directory
        
        # Hidden imports for pandas and Excel functionality
        '--hidden-import', 'pandas',
        '--hidden-import', 'openpyxl',
        '--hidden-import', 'pandas.io.excel',
        '--hidden-import', 'pandas.io.parsers',
        '--hidden-import', 'pandas.io.formats.excel',
        '--hidden-import', 'tkinter.ttk',
        '--hidden-import', 'tkinter.filedialog',
        '--hidden-import', 'tkinter.messagebox',
        
        # Add requirements file
        '--add-data', 'requirements.txt;.',
        
        # Source file
        'NameCheck_original.py'
    ]
    
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        print(f"📁 Executable location: dist{os.sep}Namechecker_1.2.exe")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        print(f"Error: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def main():
    """Main build process"""
    print("=" * 50)
    print("    📋 Namechecker v1.2")
    print("    📦 Executable Builder")
    print("=" * 50)
    print()
    
    # Check if source file exists
    if not os.path.exists('NameCheck_original.py'):
        print("❌ Error: NameCheck_original.py not found!")
        sys.exit(1)
    
    # Clean previous builds
    clean_build_files()
    print()
    
    # Build executable
    success = build_executable()
    print()
    
    if success:
        print("=" * 50)
        print("🎉 Build Process Completed Successfully!")
        print("=" * 50)
        
        # Show file info
        exe_path = Path('dist') / 'Namechecker_1.2.exe'
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📊 File size: {size_mb:.1f} MB")
            print(f"📂 Full path: {exe_path.absolute()}")
        
        print()
        print("🚀 You can now distribute Namechecker_1.2.exe")
        print("   It will work on any Windows computer without Python installed!")
    else:
        print("=" * 50)
        print("❌ Build Process Failed!")
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    main()
