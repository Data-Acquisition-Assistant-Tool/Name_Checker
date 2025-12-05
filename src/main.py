"""
NameCheck应用程序主入口
"""

import tkinter as tk
import sys
import os
import platform

def _get_resource_path(relative_path: str) -> str:
    """
    Return absolute path to resource, works for dev and for PyInstaller bundle.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base_path, relative_path)

# 添加项目根目录到Python路径，以便能够正确导入模块
# 这一步对于使用相对导入的Python包是必要的
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui.main_window import MainWindow

def main():
    """
    程序主入口函数
    """
    # Ensure Windows taskbar uses our app icon by setting AppUserModelID
    if platform.system() == 'Windows':
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Namechecker.1.5')
        except Exception:
            pass

    root = tk.Tk()

    # Set window icon (also affects taskbar on Windows when AppUserModelID is set)
    try:
        # Prefer assets/icons/namechecker.ico if available, fallback to project root
        candidate_paths = [
            _get_resource_path(os.path.join('assets', 'icons', 'namechecker.ico')),
            _get_resource_path('namechecker.ico'),
        ]
        for icon_path in candidate_paths:
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
                break
    except Exception:
        # Ignore icon errors and continue
        pass
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
