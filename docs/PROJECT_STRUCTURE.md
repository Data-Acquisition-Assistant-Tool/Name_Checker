# 项目结构说明

建议的主要目录：

- `src/`：源代码
  - `ui/`：界面相关（主窗口、结果窗口）
  - `excel_utils.py`：Excel 读取与扫描
  - `file_utils.py`：文件系统与重命名逻辑
  - `main.py`：程序入口
- `config/`：配置（窗口标题、尺寸等）
- `assets/`：静态资源
  - `icons/`：图标文件（如 `namechecker.ico`）
- `scripts/`：脚本（构建/清理等）
- `docs/`：文档
- `tests/`：测试
- `dist/`：打包产物（自动生成）
- `build/`：打包中间文件（自动生成）
- `archive/`：历史/备份

打包说明：
- 首选 `scripts/build_namechecker_1.4.bat`（标准化打包）。
- 或使用根目录的 `快速打包Namechecker.bat`。

图标查找策略：
- 运行时优先使用 `assets/icons/namechecker.ico`，若不存在回退到项目根目录的 `namechecker.ico`。

