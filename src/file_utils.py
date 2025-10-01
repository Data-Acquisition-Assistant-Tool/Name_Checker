"""
文件处理相关的工具函数
"""

import os
import re
from typing import List, Set, Dict, Optional, Tuple

from config.settings import FILENAME_PATTERN, FILES_PER_TEST

def extract_filename_base(file_name: str) -> Optional[str]:
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

def get_folder_files(folder_path: str) -> List[str]:
    """
    获取文件夹中的所有文件
    
    Args:
        folder_path: 文件夹路径
        
    Returns:
        文件夹中的文件列表
    """
    return os.listdir(folder_path)

def extract_folder_filename_bases(folder_filenames: List[str]) -> Set[str]:
    """
    从文件夹文件列表中提取符合模式的文件名基本部分
    
    Args:
        folder_filenames:
            
    Returns:
        符合模式的文件名基本部分集合
    """
    return set([extract_filename_base(f) for f in folder_filenames if extract_filename_base(f)])

def check_file_completeness(folder_path: str, folder_filenames: List[str]) -> List[str]:
    """
    检查每个测试编号是否有完整的文件集合
    
    Args:
        folder_path: 文件夹路径
        folder_filenames: 文件夹中的文件列表
        
    Returns:
        不完整的测试编号列表
    """
    # 按测试编号分组文件
    files_by_number = {}
    
    # 将文件按其基本编号分组
    for filename in folder_filenames:
        # 使用extract_filename_base函数获取完整的日期-编号字符串
        base_name = extract_filename_base(filename)
        if base_name:
            # 使用完整的日期-编号字符串作为键
            if base_name not in files_by_number:
                files_by_number[base_name] = set()
            files_by_number[base_name].add(filename)
    
    # 检查每个编号的完整性
    incomplete_numbers = []
    for number, files in files_by_number.items():
        if len(files) < FILES_PER_TEST:  # 如果文件数小于FILES_PER_TEST，则不完整
            incomplete_numbers.append(number)
    
    return incomplete_numbers 

def build_suffix_rename_plan(folder_path: str, new_suffix: str) -> Tuple[List[Tuple[str, str]], List[str], List[Tuple[str, str]]]:
    """
    基于文件名模式，生成“统一后缀”的重命名计划。

    规则：
    - 仅处理文件名中包含 FILENAME_PATTERN 的文件。
    - 将基础名（如 2025_08_18_134120）后面、扩展名之前的任意后缀，统一替换为 `_{new_suffix}`。
      例如：2025_08_18_134120_DA0097_E.blf -> 2025_08_18_134120_{new_suffix}.blf
    - 保留原始扩展名。

    Args:
        folder_path: 目标文件夹路径
        new_suffix: 期望统一成的后缀（无需前导下划线）

    Returns:
        (changes, skipped, conflicts)
        - changes: 计划变更列表 [(old_path, new_path), ...]
        - skipped: 被跳过的文件名列表（不匹配或无需修改）
        - conflicts: 与现有文件冲突的变更 [(old_path, conflict_path)]
    """
    if not new_suffix:
        raise ValueError("new_suffix 不能为空")

    # 允许用户传入包含前导下划线的后缀，统一规范为不带下划线，并在拼接时添加
    normalized_suffix = new_suffix.lstrip('_')

    folder_files = get_folder_files(folder_path)
    changes: List[Tuple[str, str]] = []
    skipped: List[str] = []
    conflicts: List[Tuple[str, str]] = []

    pattern = re.compile(FILENAME_PATTERN)

    for name in folder_files:
        # 跳过子目录，仅处理文件
        old_full_path = os.path.join(folder_path, name)
        if os.path.isdir(old_full_path):
            skipped.append(name)
            continue

        match = pattern.search(name)
        if not match:
            skipped.append(name)
            continue

        base = match.group(0)

        # 分离扩展名
        root, ext = os.path.splitext(name)

        # root 的格式一般为: 2025_08_18_134120[_第一个后缀][_额外后缀]
        # 我们需要将第一个后缀（如 DA00097_A）替换为 normalized_suffix
        # 保留后面的 _inside, _outside 等额外后缀
        
        # 找到 base 后的内容
        remaining = root[len(base):]  # 例如: _DA00097_A_inside 或 _DA00097_A
        
        if remaining:
            # 检查是否有额外后缀（如 _inside, _outside）
            # 假设第一个后缀格式是 _XXXXXXX_X，额外后缀是 _word
            parts = remaining.split('_')
            if len(parts) >= 4:  # ['', 'DA00097', 'A', 'inside'] 或 ['', 'DA00097', 'A', 'outside']
                # 有额外后缀，保留它
                extra_suffix = '_' + '_'.join(parts[3:])  # _inside 或 _outside
                new_root = f"{base}_{normalized_suffix}{extra_suffix}"
            else:
                # 没有额外后缀，只有第一个后缀
                new_root = f"{base}_{normalized_suffix}"
        else:
            # 如果 root == base，说明原来无后缀
            new_root = f"{base}_{normalized_suffix}"
            
        new_name = new_root + ext

        if new_name == name:
            # 已经是期望命名，无需修改
            skipped.append(name)
            continue

        new_full_path = os.path.join(folder_path, new_name)
        if os.path.exists(new_full_path):
            conflicts.append((old_full_path, new_full_path))
            continue

        changes.append((old_full_path, new_full_path))

    return changes, skipped, conflicts

def apply_rename_plan(changes: List[Tuple[str, str]]) -> Dict[str, object]:
    """
    执行重命名计划。

    Args:
        changes: 待执行的重命名 [(old_path, new_path)]

    Returns:
        执行统计信息字典 {"renamed": x, "failed": y, "failures": [(old, new, err_str), ...]}
    """
    renamed = 0
    failed = 0
    failures: List[Tuple[str, str, str]] = []
    for old_path, new_path in changes:
        try:
            os.rename(old_path, new_path)
            renamed += 1
        except Exception as e:
            failed += 1
            failures.append((old_path, new_path, str(e)))
    return {"renamed": renamed, "failed": failed, "failures": failures}