"""
==============================================================
File Information
    - Filename: color.py
    - Project: HeyheyEason PyREPL
    - Module: utilities.color
    - Description: File defining terminal color codes.
    - Last Modified: 2025-11-22
==============================================================
"""

from enum import Enum
from typing import ClassVar

class Color(Enum):
    """Define colors for terminal output."""
    _ignore_: ClassVar[list[str]] = ["__IS_COLOR_ENABLED"]
    __IS_COLOR_ENABLED: ClassVar[bool] = None# type: ignore[reportClassVar]

    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    @classmethod
    def setColorEnabled(cls, value: bool) -> None:
        cls.__IS_COLOR_ENABLED = value

    def __str__(self) -> str:
        """String representation of the color code."""
        if Color.__IS_COLOR_ENABLED or self == Color.RESET:
            return self.value
        else:
            return ""
