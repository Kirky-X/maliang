"""测试共用:加载 scripts/ 下带连字符文件名的模块。

用法:
    from _load import load
    vdm = load("validate-draw-md.py")
"""

import importlib.util
import os
import sys

SCRIPTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "scripts")
)


def load(filename):
    """按文件名加载 scripts/ 下模块,返回 module 对象。"""
    # 被加载脚本内部 `import maliang_common` 依赖 scripts/ 在 sys.path 上
    if SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, SCRIPTS_DIR)
    path = os.path.join(SCRIPTS_DIR, filename)
    mod_name = filename.replace(".py", "").replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path, text):
    """测试共享写入:父目录自动创建,UTF-8 落盘。path 接受 str 或 Path,返回 str 路径。"""
    from pathlib import Path

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return str(path)
