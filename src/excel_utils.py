"""
Excel处理相关的工具函数
"""

import re
import pandas as pd
from typing import List, Tuple, Set, Dict, Union

from config.settings import FILENAME_PATTERN

def split_filenames(cell_value):
    """
    使用多种分隔符分割单元格内容
    
    Args:
        cell_value: 单元格内容
        
    Returns:
        分割后的文件名列表
    """
    if isinstance(cell_value, str):
        # 使用常见分隔符：换行符、逗号、分号、空格
        delimiters = r'[\n,; ]+'
        return re.split(delimiters, cell_value)
    return []

def scan_excel_for_filenames(df: pd.DataFrame) -> Tuple[pd.Series, List[str], int]:
    """
    扫描整个Excel表格，找出所有符合模式的文件名
    
    Args:
        df: pandas DataFrame对象
        
    Returns:
        Tuple包含：
        - 所有唯一的文件名（pandas.Series）
        - 重复的文件名列表
        - 不同测试编号的数量
    """
    all_filenames = []
    for col in df.columns:
        column_data = df[col].dropna().apply(split_filenames).explode()
        column_filenames = column_data.apply(lambda x: extract_filename_base(str(x))).dropna()
        all_filenames.extend(column_filenames)
    
    # 转换为Series并找出重复项
    filename_series = pd.Series(all_filenames)
    duplicates = filename_series[filename_series.duplicated()].unique()
    unique_filenames = filename_series.drop_duplicates()
    
    # 计算不同的测试编号数量
    test_numbers = set()
    for filename in all_filenames:
        if filename:
            test_number = filename[-6:]  # 获取文件名最后6位数字
            test_numbers.add(test_number)
    
    return unique_filenames, duplicates.tolist(), len(test_numbers)

def extract_filename_base(file_name: str) -> str:
    """
    提取文件名中符合模式的基本部分 (20xx_xx_xx_xxxxxx)
    
    Args:
        file_name: 待处理的文件名
        
    Returns:
        匹配的文件名基本部分，如果没有匹配则返回None
    """
    match = re.search(FILENAME_PATTERN, file_name)
    if match:
        return match.group(0)  # 返回匹配的模式
    return None

def get_excel_sheets(file_path: str) -> List[str]:
    """
    获取Excel文件的所有sheet名称
    
    Args:
        file_path: Excel文件路径
        
    Returns:
        sheet名称列表
    """
    return pd.ExcelFile(file_path).sheet_names

def _column_letter_to_index(column_ref: str) -> int:
    """
    Convert Excel-style column letters (e.g., 'A', 'L') to zero-based indices.
    """
    if not column_ref or not column_ref.strip():
        raise ValueError("Column reference cannot be empty")
    ref = column_ref.strip().upper()
    if not ref.isalpha():
        raise ValueError(f"Invalid column reference: {column_ref}")
    index = 0
    for ch in ref:
        index = index * 26 + (ord(ch) - ord('A') + 1)
    return index - 1


def _resolve_column(df: pd.DataFrame, column_ref: Union[str, int]):
    """
    Resolve pandas column using Excel column notation, integer index, or explicit column name.
    """
    if isinstance(column_ref, int):
        return df.iloc[:, column_ref]
    if isinstance(column_ref, str):
        stripped = column_ref.strip()
        if stripped.upper().isalpha():
            idx = _column_letter_to_index(stripped)
            if idx >= len(df.columns):
                raise ValueError(f"Sheet does not contain column {column_ref}")
            return df.iloc[:, idx]
        if stripped in df.columns:
            return df[stripped]
    raise ValueError(f"Unsupported column reference: {column_ref}")


def _normalize_group_value(value) -> str:
    """
    Normalize numeric/text cell values so they can be used as folder names.
    """
    if pd.isna(value):
        return ""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if float(value).is_integer():
            return str(int(value))
        return str(value).strip()
    return str(value).strip()


def build_group_mapping_from_excel(df: pd.DataFrame, group_column="L", names_column="M"):
    """
    Build mapping between filenames (column M) and group labels (column L).

    Returns:
        (filename_to_group, group_to_names)
    """
    filename_to_group: Dict[str, str] = {}
    group_to_names: Dict[str, Set[str]] = {}
    group_series = _resolve_column(df, group_column)
    names_series = _resolve_column(df, names_column)
    for group_value, names_cell in zip(group_series, names_series):
        label = _normalize_group_value(group_value)
        if not label:
            continue
        filenames = split_filenames(names_cell)
        cleaned = [s.strip() for s in filenames if isinstance(s, str) and s.strip()]
        if not cleaned:
            continue
        for name in cleaned:
            filename_to_group[name] = label
            group_to_names.setdefault(label, set()).add(name)
    if not filename_to_group:
        raise ValueError("No filenames found in the specified Excel columns")
    return filename_to_group, group_to_names

