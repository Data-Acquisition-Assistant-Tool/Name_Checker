"""
Main window UI components
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

from config.settings import WINDOW_TITLE
from src.file_utils import (
    get_folder_files,
    extract_folder_filename_bases,
    check_file_completeness,
    build_suffix_rename_plan,
    apply_rename_plan,
)
from src.excel_utils import get_excel_sheets, scan_excel_for_filenames
from src.ui.result_window import ResultWindow

class MainWindow:
    """
    Main window class, responsible for file selection and comparison operations
    """
    def __init__(self, root):
        """
        Initialize main window
        
        Args:
            root: tkinter root window
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        
        # Save paths
        self.excel_path_var = tk.StringVar()
        self.folder_path_var = tk.StringVar()
        self.sheet_var = tk.StringVar()
        # Unified suffix input
        self.rename_suffix_var = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """
        Setup UI components
        """
        # Excel file selection
        tk.Label(self.root, text="Select Excel File:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.excel_path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.select_excel_file).grid(row=0, column=2, padx=10, pady=10)
        
        # Sheet selection
        tk.Label(self.root, text="Select Sheet:").grid(row=1, column=0, padx=10, pady=10)
        self.sheet_menu = tk.OptionMenu(self.root, self.sheet_var, '')  # default empty menu
        self.sheet_menu.grid(row=1, column=1, padx=10, pady=10)
        
        # Folder selection
        tk.Label(self.root, text="Select Folder:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.folder_path_var, width=50).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.select_folder).grid(row=2, column=2, padx=10, pady=10)
        
        # Start comparison button
        tk.Button(self.root, text="Start Comparison", command=self.compare_files).grid(row=3, column=1, padx=10, pady=10)

        # Unified suffix - input and buttons
        ttk.Separator(self.root, orient='horizontal').grid(row=4, column=0, columnspan=3, sticky='ew', padx=10, pady=(5,5))
        tk.Label(self.root, text="Unified Suffix:").grid(row=5, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.rename_suffix_var, width=20).grid(row=5, column=1, padx=10, pady=5, sticky='w')
        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=6, column=1, pady=10)
        tk.Button(btn_frame, text="Preview Rename", command=self.preview_rename).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Apply Rename", command=self.execute_rename).pack(side=tk.LEFT, padx=5)
    
    def select_excel_file(self):
        """
        Select Excel file
        """
        file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx")])
        self.excel_path_var.set(file_path)
        if file_path:
            try:
                # Read all sheet names from Excel file
                sheet_names = get_excel_sheets(file_path)
                self.sheet_var.set(sheet_names[0])  # default select first sheet
                self.sheet_menu['menu'].delete(0, 'end')  # clear old menu
                for sheet in sheet_names:
                    self.sheet_menu['menu'].add_command(label=sheet, command=tk._setit(self.sheet_var, sheet))
            except Exception as e:
                messagebox.showerror("Error", f"Cannot read sheets from Excel: {str(e)}")
    
    def select_folder(self):
        """
        Select folder
        """
        folder_path = filedialog.askdirectory(title="Select Folder")
        self.folder_path_var.set(folder_path)
    
    def compare_files(self):
        """
        Compare files
        """
        excel_file_path = self.excel_path_var.get()
        folder_path = self.folder_path_var.get()
        selected_sheet = self.sheet_var.get()
        
        if not excel_file_path or not folder_path:
            messagebox.showerror("Error", "Please select Excel file and folder again")
            return
        
        try:
            # Read selected Excel sheet
            df = pd.read_excel(excel_file_path, sheet_name=selected_sheet)
            
            # Scan entire Excel for filenames matching pattern and get duplicates
            excel_filenames, duplicates, test_count = scan_excel_for_filenames(df)
            
            # Get file list from folder
            folder_filenames = get_folder_files(folder_path)
            
            # Extract relevant filenames from folder and use set to remove duplicates
            folder_filenames_base = extract_folder_filename_bases(folder_filenames)
            
            # Compare filenames (only match patterns)
            excel_not_in_folder = excel_filenames[~excel_filenames.isin(folder_filenames_base)]
            folder_not_in_excel = [f for f in folder_filenames_base if f not in excel_filenames.values]
            
            # Check file completeness
            incomplete_files = check_file_completeness(folder_path, folder_filenames)
            
            result = ""
            has_issues = False
            
            # In Excel but not in folder
            if not excel_not_in_folder.empty:
                has_issues = True
                # Sort by time (lexicographic works for pattern like YYYY_MM_DD_HHMMSS)
                excel_missing_list = list(excel_not_in_folder.sort_values())
                result += f"In Excel but not in folder ({len(excel_missing_list)}):\n"
                result += "\n".join(excel_missing_list) + "\n\n"
            
            # In folder but not in Excel
            if folder_not_in_excel:
                has_issues = True
                # Sort by time (same rationale)
                folder_only_list = sorted(folder_not_in_excel)
                result += f"In folder but not in Excel ({len(folder_only_list)}):\n"
                result += "\n".join(folder_only_list) + "\n\n"
            
            # Add incomplete file information
            if incomplete_files:
                has_issues = True
                result += "Incomplete file numbers (less than 4 files):\n"
                result += ", ".join(incomplete_files) + "\n\n"
            
            # Add duplicate file information
            if duplicates:
                has_issues = True
                result += "Duplicate filenames found in Excel:\n"
                result += "\n".join(duplicates) + "\n\n"
            else:
                result += "No duplicate filenames found in Excel.\n\n"
            
            # If no issues found, show complete success message
            if not has_issues:
                result = "All numbers have complete file sets (4 files each), Excel and folder match.\nNo duplicate filenames found in Excel."
            
            # Add test count information at the beginning of result
            result = f"Current Excel file ({selected_sheet}) has {test_count} different test numbers.\n\n" + result
            
            # 显示结果窗口
            ResultWindow(self.root, result)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}") 

    def _require_folder_selected(self) -> str:
        folder_path = self.folder_path_var.get()
        if not folder_path:
            messagebox.showerror("Error", "Please select a folder first")
            return ""
        return folder_path

    def preview_rename(self):
        """
        Preview rename plan for unified suffix
        """
        folder_path = self._require_folder_selected()
        if not folder_path:
            return
        suffix = self.rename_suffix_var.get().strip()
        if not suffix:
            messagebox.showerror("Error", "Please enter the suffix to unify, e.g. H022296_E or E")
            return
        try:
            changes, skipped, conflicts = build_suffix_rename_plan(folder_path, suffix)
            lines = []
            lines.append(f"Target folder: {folder_path}")
            lines.append(f"Unified suffix: {suffix}")
            lines.append("")
            lines.append(f"Will rename {len(changes)} files:")
            for old_p, new_p in changes[:500]:
                lines.append(f"{os.path.basename(old_p)}  ->  {os.path.basename(new_p)}")
            if len(changes) > 500:
                lines.append(f"... remaining {len(changes) - 500} not shown")
            lines.append("")
            if conflicts:
                lines.append(f"Detected {len(conflicts)} name conflicts (will not be applied):")
                for old_p, new_p in conflicts[:200]:
                    lines.append(f"Conflict: {os.path.basename(old_p)} -> {os.path.basename(new_p)} already exists")
                if len(conflicts) > 200:
                    lines.append(f"... remaining {len(conflicts) - 200} not shown")
                lines.append("")
            lines.append(f"Skipped {len(skipped)} items (non-matching, already correct, or directories)")
            ResultWindow(self.root, "\n".join(lines))
        except Exception as e:
            messagebox.showerror("Error", f"Preview failed: {str(e)}")

    def execute_rename(self):
        """
        Apply rename with unified suffix
        """
        folder_path = self._require_folder_selected()
        if not folder_path:
            return
        suffix = self.rename_suffix_var.get().strip()
        if not suffix:
            messagebox.showerror("Error", "Please enter the suffix to unify")
            return
        try:
            changes, skipped, conflicts = build_suffix_rename_plan(folder_path, suffix)
            if not changes:
                messagebox.showinfo("Info", "No files need to be renamed")
                return
            if conflicts:
                messagebox.showwarning("Warning", f"There are {len(conflicts)} name conflicts, they will be skipped")
            if not messagebox.askyesno("Confirm", f"Apply rename to {len(changes)} files?"):
                return
            stats = apply_rename_plan(changes)
            message = (
                f"Rename completed\n\n"
                f"Success: {stats['renamed']}\n"
                f"Failed: {stats['failed']}\n"
                f"Conflicts skipped: {len(conflicts)}\n"
                f"Other skipped: {len(skipped)}"
            )
            if stats.get('failed'):
                # 分析失败原因并给出简洁说明
                failure_reasons = {}
                for old_p, new_p, err in stats.get('failures', []):
                    if "already exists" in err or "bereits vorhanden" in err:
                        reason = "Target file already exists (conflict)"
                    elif "Permission denied" in err or "Access is denied" in err:
                        reason = "Permission denied (file in use)"
                    elif "cannot find" in err:
                        reason = "Source file not found"
                    else:
                        reason = f"Other error: {err[:50]}..."
                    
                    if reason not in failure_reasons:
                        failure_reasons[reason] = 0
                    failure_reasons[reason] += 1
                
                # 构建详细消息
                detail_msg = message + "\n\nFailure reasons:\n"
                for reason, count in failure_reasons.items():
                    detail_msg += f"- {reason}: {count} files\n"
                
                messagebox.showinfo("Done", detail_msg)
            else:
                messagebox.showinfo("Done", message)
        except Exception as e:
            messagebox.showerror("Error", f"Apply failed: {str(e)}")