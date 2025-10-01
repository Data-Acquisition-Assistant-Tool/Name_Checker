# NameCheck - File Name Check Tool

A comprehensive tool for comparing filenames between Excel files and folders, with batch renaming capabilities.

## Features

### Core Comparison Features
- Extract filenames matching specific patterns from Excel files
- Check file completeness (each test number should have required number of files)
- Compare filenames between Excel and folder
- Detect duplicate filenames in Excel
- Display count of different test numbers
- Support for multiple Excel sheets

### Batch Renaming Features
- **Unified Suffix Renaming**: Batch rename files to use a unified suffix
- **Smart Pattern Recognition**: Automatically detects date-based filename patterns (`20xx_xx_xx_xxxxxx`)
- **Preserve Additional Suffixes**: Keeps `_inside`, `_outside`, etc. when renaming
- **Preview Before Apply**: Preview all changes before executing
- **Conflict Detection**: Identifies and reports naming conflicts
- **Detailed Error Reporting**: Shows specific reasons for any failures

### Result Management
- Add suffixes to result filenames
- Copy results with or without line breaks
- Resizable result window with scrollbars
- Undo changes functionality

## Project Structure

```
NameCheck/
│
├── src/                    # Source code
│   ├── main.py             # Main application entry
│   ├── file_utils.py       # File processing utilities
│   ├── excel_utils.py      # Excel processing utilities
│   └── ui/                 # User interface
│       ├── main_window.py  # Main window
│       └── result_window.py # Result display window
│
├── config/                 # Configuration
│   └── settings.py         # Application settings
│
├── archive/                # Archived files
│   └── NameCheck_legacy.py # Original single-file version
│
├── tests/                  # Test files
│   └── __init__.py
│
├── Namecheck.py            # Application launcher
├── requirements.txt        # Dependencies
├── build_detailed.py       # Build script
├── build_exe.bat          # Build batch file
├── 快速打包Namechecker.bat # Quick build script
├── Namechecker_1.2.spec   # PyInstaller spec
└── README.md              # This file
```

## Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
```bash
python Namecheck.py
```

### Basic File Comparison
1. Select Excel file (.xlsx format)
2. Choose sheet to compare
3. Select folder to compare
4. Click "Start Comparison"
5. Review results in the popup window

### Batch Renaming
1. Select target folder
2. Enter unified suffix (e.g., `H022295_E`)
3. Click "Preview Rename" to see planned changes
4. Click "Apply Rename" to execute changes

### Filename Format
The tool recognizes filenames with this pattern:
- Format: `20xx_xx_xx_xxxxxx[_suffix][_additional]`
- Examples:
  - `2025_04_15_155131_DA00097_A.blf`
  - `2025_04_15_155131_DA00097_A_inside.mp4`
  - `2025_04_15_155131_DA00097_A_outside.mp4`

### Renaming Examples
- `2025_04_15_155131_DA00097_A.blf` → `2025_04_15_155131_H022295_E.blf`
- `2025_04_15_155131_DA00097_A_inside.mp4` → `2025_04_15_155131_H022295_E_inside.mp4`
- `2025_04_15_155131_DA00097_A_outside.mp4` → `2025_04_15_155131_H022295_E_outside.mp4`

## Configuration

Edit `config/settings.py` to modify:
- Filename pattern matching
- Minimum files required per test number
- Window titles and dimensions

## Building Executable

### Quick Build
```bash
./快速打包Namechecker.bat
```

### Detailed Build
```bash
python build_detailed.py
```

## Dependencies

- Python 3.6+
- pandas
- openpyxl
- tkinter (included with Python)

## Error Handling

The tool provides detailed error reporting for rename operations:
- **Target file already exists**: File naming conflicts
- **Permission denied**: File in use or access issues
- **Source file not found**: File moved or deleted
- **Other errors**: Additional error details

## Version History

- **v1.3**: Enhanced UI with resizable result window and improved error reporting
- **v1.2**: Added batch renaming with unified suffix support
- **v1.1**: Modular architecture with improved UI
- **v1.0**: Basic file comparison functionality

## License

MIT License

## Notes

- Ensure Excel files are in .xlsx format
- The tool only processes files matching the date pattern
- Preview functionality helps avoid unintended changes
- Original files are archived in the `archive/` directory