"""
==============================================================
File Information
    - Filename: color.py
    - Project: HeyheyEason PyREPL
    - Module: utilities.color
    - Description: File defining terminal color codes.
    - Last Modified: 2025-11-09
==============================================================
"""

from enum import Enum

class Color(Enum):
    """Define colors for terminal output."""
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    def __str__(self) -> str:
        """String representation of the color code."""
        return self.value