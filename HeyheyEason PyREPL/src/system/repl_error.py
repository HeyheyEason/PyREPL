"""
==============================================================
File Information
    - Filename: repl_error.py
    - Project: HeyheyEason PyREPL
    - Module: system.repl_error
    - Description: File defining ReplError class.
    - Last Modified: 2025-11-22
==============================================================
"""

class ReplError(BaseException):
    """An exception for PyREPL's fatal error"""
    
    def __init__(self, msg: str, error_code: int=None, context_data: str=None) -> None:
        super().__init__(msg)
        self.error_code: int = error_code if error_code is not None else -1
        self.context_data: str = context_data if context_data is not None else ""

    def __str__(self) -> str:
        """Turn the exception instance into string."""
        base_message: str = super().__str__()
        output: str = f"PyRepl Fatal Error: {base_message} <Code: {self.error_code} ({hex(self.error_code)})>\n" + \
                      f"Reason: {self.context_data}"
        return output