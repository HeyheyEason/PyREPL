"""
==============================================================
File Information
    - Filename: __init__.py
    - Project: HeyheyEason PyREPL
    - Module: system
    - Description: The initizlizer of non-core system module.
    - Last Modified: 2025-11-22
==============================================================
"""

from .config import Config
from .repl_error import ReplError

__all__: list[str] = ["Config", "ReplError"]