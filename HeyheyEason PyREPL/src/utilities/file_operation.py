"""
==============================================================
File Information
    - Filename: file_operation.py
    - Project: HeyheyEason PyREPL
    - Module: utilities.file_operation
    - Description: File defining file operations for scripts.
    - Last Modified: 2025-11-09
==============================================================
"""

from enum import Enum

class FileOperation(Enum):
    """Define file operations for script handling."""
    IDLING = 0
    WRITE = 1
    APPEND = 2
    READ = 3
    DELETE = 4
