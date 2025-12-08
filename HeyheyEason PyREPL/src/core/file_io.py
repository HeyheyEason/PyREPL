"""
==============================================================
File Information
    - Filename: file_io.py
    - Project: HeyheyEason PyREPL
    - Module: core.file_io
    - Description: Script for file I/O operations in the REPL.
    - Last Modified: 2025-11-22
==============================================================
"""

import sys
import webbrowser
from typing import ClassVar, Optional
from pathlib import Path
from io import TextIOWrapper
from utilities import FileOperation, Color
from system import Config

class FileIO:
    """Class representing file input/output system for the REPL."""
    
    # Define base directory paths
    HELP_DIR: ClassVar[Path] = None
    SCRIPTS_DIR: ClassVar[Path] = None
    LOGS_DIR: ClassVar[Path] = None

    PYTHON_VERSION_INFO: ClassVar[str] = f"{sys.version_info.major}.{sys.version_info.minor}"
    PYTHON_DOCS_URL: ClassVar[str] = f"https://docs.python.org/{PYTHON_VERSION_INFO}/"

    def __init__(self) -> None:
        """Class initailizer for FileIO."""
        self.script_file: Optional[TextIOWrapper] = None
        self.file_operation: FileOperation = FileOperation.IDLING

    @classmethod
    def setConstants(cls, file_config: dict) -> None:
        dir_config: dict = file_config.get('dir', {})

        cls.HELP_DIR = Config.PROJECT_DIR / dir_config.get('help', "data/assets/Help.txt")
        cls.LOGS_DIR = Config.PROJECT_DIR / dir_config.get('logs', "data/logs")

        if file_config.get('use-default-scripts-dir', True):
            cls.SCRIPTS_DIR = Config.PROJECT_DIR / dir_config.get('scripts-default', "data/scripts")
        else:
            cls.SCRIPTS_DIR = Config.PROJECT_DIR / dir_config.get('scripts-custom', "")

    @classmethod
    def getHelp(cls, keyword: str) -> None:
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
            url: str = f"{cls.PYTHON_DOCS_URL}search.html?q={keyword}"

            try:
                webbrowser.open_new_tab(url)
                print(f"{Color.CYAN}Opening web browser for Python documentation on '{keyword}'...{Color.RESET}\n")
            except webbrowser.Error as e:
                print(f"{Color.RED}PyREPL Error: Failed to open web browser. {e}{Color.RESET}\n")
            
            return

        chapter_name: str = chapter[keyword]

        try:
            with open(cls.HELP_DIR, "r", encoding="utf-8") as help_file:
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
            print(f"{Color.RED}PyREPL Error: Help file not found.{Color.RESET}\n")

    def openFile(self, op: str, file_name: str) -> bool:
        """Initialize the script file."""
        if self.file_operation != FileOperation.IDLING:
            print(f"{Color.RED}PyREPL Error: A file is already open. Please close it before opening another file.{Color.RESET}\n")
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
                print(f"{Color.RED}PyREPL Error: File '{script_path}' not found.{Color.RESET}\n")
                self.file_operation = FileOperation.IDLING
                return False
        elif self.file_operation == FileOperation.DELETE:
            if script_path.exists():
                script_path.unlink()
                self.file_operation = FileOperation.IDLING
                print(f"{Color.CYAN}File '{script_path}' deleted successfully.{Color.RESET}\n")
            else:
                self.file_operation = FileOperation.IDLING
                print(f"{Color.RED}File '{script_path}' not found.{Color.RESET}\n")
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
