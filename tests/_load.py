"""测试共用:加载 scripts/ 下带连字符文件名的模块。

用法:
    from _load import load
    vdm = load("validate-draw-md.py")
"""

import importlib.util
import os

SCRIPTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "scripts")
)


def load(filename):
    """按文件名加载 scripts/ 下模块,返回 module 对象。"""
    path = os.path.join(SCRIPTS_DIR, filename)
    mod_name = filename.replace(".py", "").replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
