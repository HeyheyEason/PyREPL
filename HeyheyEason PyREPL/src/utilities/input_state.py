"""
==============================================================
File Information
    - Filename: input_state.py
    - Project: HeyheyEason PyREPL
    - Module: utilities.input_state
    - Description: File defining input states for the REPL.
    - Last Modified: 2025-11-09
==============================================================
"""

from enum import Enum

class InputState(Enum):
    """Define input states for the REPL."""
    SINGLE_LINE = 1
    MULTI_LINE = 2
    AWAITING_MORE = 3