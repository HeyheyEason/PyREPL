"""
==============================================================
File Information
    - Filename: file_io.py
    - Project: HeyheyEason PyREPL
    - Module: core.file_io
    - Description: Script for file I/O operations in the REPL.
    - Last Modified: 2025-11-12
==============================================================
"""

import sys
import webbrowser
from pathlib import Path
from io import TextIOWrapper
from utilities import FileOperation, Color

class FileIO:
    """Class representing file input/output system for the REPL."""
    
    # Define base directory paths
    PROJECT_DIR: Path = Path(sys.executable).resolve().parent.parent.parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent.parent.parent
    HELP_DIR: Path = PROJECT_DIR / "data" / "documents" / "Help.txt"
    SCRIPTS_DIR: Path = PROJECT_DIR / "data" / "scripts"

    PYTHON_VERSION_INFO: str = f"{sys.version_info.major}.{sys.version_info.minor}"
    PYTHON_DOCS_URL: str = f"https://docs.python.org/{PYTHON_VERSION_INFO}/"

    def __init__(self) -> None:
        """Class initailizer for FileIO."""
        self.script_file: TextIOWrapper = None
        self.file_operation: FileOperation = FileOperation.IDLING

    def getHelp(self, keyword: str) -> None:
        """Print help information."""
        keyword = keyword.replace('"', '').replace('\'', '')
        chapter: dict[str, str] = {
            "all": "all",
            "intro": "PyREPL User Manual",
            "cmdline-args": "Command Line Arguments",
            "internal-cmds": "Internal Commands",
            "coding": "Coding",
            "examples": "Long Code Examples",
            "note": "Note"
        }

        if keyword not in chapter:
            url: str = f"{FileIO.PYTHON_DOCS_URL}search.html?q={keyword}"

            try:
                webbrowser.open_new_tab(url)
                print(f"{Color.CYAN}Opening web browser for Python documentation on '{keyword}'...{Color.RESET}")
            except webbrowser.Error as e:
                print(f"{Color.RED}PyREPL Error: Failed to open web browser. {e}{Color.RESET}")
            
            return

        chapter_name: str = chapter[keyword]

        try:
            with open(FileIO.HELP_DIR, "r", encoding="utf-8") as help_file:
                if chapter_name == "all":
                    help_text: list[str] = help_file.read().splitlines()
                else:
                    help_text: list[str] = ["-" * 80]
                    correct_chapter: bool = False

                    for raw_line in help_file:
                        help_line: str = raw_line.replace('\n', '')

                        if help_line.startswith(chapter_name):
                            correct_chapter = True

                        if correct_chapter:
                            help_text.append(help_line)

                            if help_line.endswith("---"):
                                break

            input(f"{Color.CYAN}Press Enter to show the next line, type 'return' to return to the REPL...{Color.RESET}")

            for line in help_text:
                help_operation: str = input(line).lower().strip()

                if help_operation == "return" or help_operation == "r":
                    return

            input(f"{Color.CYAN}Press Enter to continue...{Color.RESET}")
        except FileNotFoundError:
            print(f"{Color.RED}PyREPL Error: Help file not found.{Color.RESET}")

    def openFile(self, op: str, file_name: str) -> bool:
        """Initialize the script file."""
        if self.file_operation != FileOperation.IDLING:
            print(f"{Color.RED}PyREPL Error: A file is already open. Please close it before opening another file.{Color.RESET}")
            return False

        script_path: Path = FileIO.SCRIPTS_DIR / file_name
        op_dict: dict[str, FileOperation] = {
            "write": FileOperation.WRITE,
            "append": FileOperation.APPEND,
            "read": FileOperation.READ,
            "delete": FileOperation.DELETE
        }

        self.file_operation: FileOperation = op_dict[op]

        if self.file_operation == FileOperation.WRITE:
            self.script_file = open(script_path, "w", encoding="utf-8")
        elif self.file_operation == FileOperation.APPEND:
            self.script_file = open(script_path, "a", encoding="utf-8")
        elif self.file_operation == FileOperation.READ:
            if script_path.exists():
                self.script_file = open(script_path, "r", encoding="utf-8")
            else:
                print(f"{Color.RED}PyREPL Error: File '{script_path}' not found.{Color.RESET}")
                self.file_operation = FileOperation.IDLING
                return False
        elif self.file_operation == FileOperation.DELETE:
            if script_path.exists():
                script_path.unlink()
                self.file_operation = FileOperation.IDLING
                print(f"{Color.CYAN}File '{script_path}' deleted successfully.{Color.RESET}")
            else:
                self.file_operation = FileOperation.IDLING
                print(f"{Color.RED}File '{script_path}' not found.{Color.RESET}")
                return False

        return True

    def closeFile(self) -> None:
        """Close the script file if it's open."""
        if self.script_file is not None:
            self.script_file.close()
            self.script_file = None
            self.file_operation = FileOperation.IDLING

    def write(self, code_str: str) -> bool:
        """Write input based on the file operation."""
        if self.file_operation == FileOperation.IDLING:
            return False
        elif self.file_operation == FileOperation.WRITE or self.file_operation == FileOperation.APPEND:
            self.script_file.write(code_str + "\n")
            return True

    def read(self) -> str:
        """Read the content of the script file."""
        raw_line: str = self.script_file.readline()

        # End of file
        if not raw_line:
            return ""

        # Skip empty lines
        if raw_line.strip() == "":
            return self.read()
        else:
            return raw_line.rstrip()