"""
==================================================================================================================
File Information
    - Filename: main.py
    - Project: HeyheyEason PyREPL
    - Module: __main__
    - Author: HeyheyEason
    - License: MIT License
    - Description: The main entry point for PyREPL.
    - Version: 3.0.0
    - Last Modified: 2025-11-22
------------------------------------------------------------------------------------------------------------------
Environment Information
    - Python Version: 3.13.9
    - OS: Cross-platform (Windows, macOS, Linux)
    - Terminal: ANSI-compatible terminal recommended
------------------------------------------------------------------------------------------------------------------
Changelog
    - 3.0.0:
        1. Submitter: Eason Huang
        2. Contents:
            a. The config editor is now availavle, controlling configuration of the app.
            b. The prompts can now be modified in config.json.
            c. Improved the compatibility with older terminals through providing an option to disable color texts.
            d. Ctrl+C is used to cancel the input now, not terminate the REPL.
            e. The output on the screen will now be separated with a empty line.
            f. Fix a bug that cause improper position of the prompt when user's 'print()' ends with non-\n chars.
==================================================================================================================
"""

import sys
from core import Repl
from utilities import Color
from system import ReplError

def main(argv: list[str]) -> int:
    """The entry point for PyREPL."""
    if "--version" in argv or "-v" in argv:
        Repl.printVersion()
        return 0
    elif "--credits" in argv or "-c" in argv:
        Repl.printCredits()
        return 0
    else:
        try:
            repl: Repl = Repl()
            repl.run()
            repl.file_io.closeFile()
            return 0
        except ReplError as e:
            print(f"{Color.RED}{e}{Color.RESET}")
            return e.error_code
        except BaseException:
            repl.handleTermination()
            return 4

if __name__ == "__main__":
    sys.exit(main(sys.argv))