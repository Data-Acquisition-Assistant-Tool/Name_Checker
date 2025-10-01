"""
Result window UI components
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config.settings import RESULT_WINDOW_TITLE, RESULT_WINDOW_WIDTH, RESULT_WINDOW_HEIGHT

class ResultWindow:
    """
    Window class for displaying comparison results
    """
    def __init__(self, parent, result_text):
        """
        Initialize result window
        
        Args:
            parent: parent window
            result_text: result text to display
        """
        self.window = tk.Toplevel(parent)
        self.window.title(RESULT_WINDOW_TITLE)
        self.window.geometry(f"{RESULT_WINDOW_WIDTH}x{RESULT_WINDOW_HEIGHT}")
        
        # 设置窗口可调整大小
        self.window.resizable(True, True)
        self.window.minsize(400, 300)  # 设置最小尺寸

        # Save original text for undo
        self.original_text = result_text

        # Add input box and button frame
        self.input_frame = ttk.Frame(self.window)
        self.input_frame.pack(pady=5)
        
        # Add input box
        self.suffix_var = tk.StringVar()
        ttk.Label(self.input_frame, text="Add suffix:").pack(side=tk.LEFT, padx=5)
        self.suffix_entry = ttk.Entry(self.input_frame, textvariable=self.suffix_var)
        self.suffix_entry.pack(side=tk.LEFT, padx=5)
        
        # Add apply suffix button and undo button
        ttk.Button(self.input_frame, text="Apply Suffix", command=self.apply_suffix).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.input_frame, text="Undo", command=self.undo_changes).pack(side=tk.LEFT, padx=5)

        # Create text box with scrollbars and dynamic sizing
        text_frame = tk.Frame(self.window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建滚动条
        v_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
        h_scrollbar = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        
        # 创建文本框
        self.text_widget = tk.Text(
            text_frame, 
            wrap=tk.NONE,  # 不自动换行，让水平滚动条处理
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            font=('Consolas', 9)  # 使用等宽字体，便于对齐
        )
        self.text_widget.insert(tk.END, result_text)
        
        # 配置滚动条
        v_scrollbar.config(command=self.text_widget.yview)
        h_scrollbar.config(command=self.text_widget.xview)
        
        # 布局
        self.text_widget.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # 配置网格权重，让文本框可以扩展
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Create button frame
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=5)
        
        # Add copy buttons
        ttk.Button(button_frame, text="Copy Results (Keep Line Breaks)", command=self.copy_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Copy as Single Line", command=self.copy_as_single_line).pack(side=tk.LEFT, padx=5)

    def apply_suffix(self):
        """
        Add suffix to all filenames
        """
        suffix = self.suffix_var.get()
        if suffix:
            # Get all text content
            content = self.text_widget.get("1.0", tk.END).strip()
            lines = content.split('\n')
            
            # Process each line
            new_content = []
            for line in lines:
                if line.strip() and not line.startswith("In Excel") and not line.startswith("In Folder"):
                    line = line + suffix
                new_content.append(line)
            
            # Update text box content
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", '\n'.join(new_content))

    def undo_changes(self):
        """
        Undo changes, restore original text
        """
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", self.original_text)

    def copy_text(self):
        """
        Copy text (keep line breaks)
        """
        self.window.clipboard_clear()
        self.window.clipboard_append(self.text_widget.get("1.0", tk.END))
        messagebox.showinfo("Success", "Results copied to clipboard!")

    def copy_as_single_line(self):
        """
        Copy as single line (remove line breaks and title lines)
        """
        content = self.text_widget.get("1.0", tk.END).strip()
        lines = content.split('\n')
        
        # Filter out title lines and empty lines, keep only filenames, remove all whitespace
        filenames = [line.strip() for line in lines 
                    if line.strip() and not line.startswith("In Excel") and not line.startswith("In folder")]
        
        # Directly connect all filenames (no separators)
        single_line = ''.join(filenames)
        
        # Ensure all possible line breaks are removed
        single_line = single_line.replace('\n', '').replace('\r', '')
        
        self.window.clipboard_clear()
        self.window.clipboard_append(single_line)
        messagebox.showinfo("Success", "Results copied as single line!")