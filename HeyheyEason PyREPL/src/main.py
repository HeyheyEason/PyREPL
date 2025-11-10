"""
==================================================================================================
File Information
    - Filename: main.py
    - Project: HeyheyEason PyREPL
    - Module: __main__
    - Author: HeyheyEason
    - License: MIT License
    - Description: The main entry point for the PyREPL app.
    - Version: 2.1.1
    - Last Modified: 2025-11-09
--------------------------------------------------------------------------------------------------
Environment Information
    - Python Version: 3.13.8
    - OS: Cross-platform (Windows, macOS, Linux)
    - Terminal: ANSI-compatible terminal recommended
--------------------------------------------------------------------------------------------------
Changelog
    - 2.1.1:
        1. Submitter: Eason Huang
        2. Changes:
            a. Refactored codebase for improved modularity and maintainability.
    - 2.1.0:
        1. Submitter: Eason Huang
        2. Changes:
            a. 'help()' function has been removed due to the executable file limitation.
            b. 'help' command can now be used to search Python documentation online.
==================================================================================================
"""

import sys
from core import Repl

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
        except KeyboardInterrupt:
            repl.file_io.closeFile()
            return 1
        except BaseException:
            repl.handleTermination()
            return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))