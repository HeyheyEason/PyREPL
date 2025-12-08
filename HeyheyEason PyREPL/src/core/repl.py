"""
==============================================================
File Information
    - Filename: repl.py
    - Project: HeyheyEason PyREPL
    - Module: core.repl
    - Description: The implementation of the REPL.
    - Last Modified: 2025-11-22
==============================================================
"""

import os
import platform
from typing import ClassVar
from types import CodeType
from .file_io import FileIO
from utilities import InputState, Color
from system import Config

class Repl:
    """Class representing the REPL environnemt."""

    # Define REPL basic information
    AUTHOR: ClassVar[str] = None
    VERSION: ClassVar[list[int]] = None

    # Define indentation step
    INDENT_STEP: ClassVar[int] = None

    # Define prompt strings with colors
    PRIMARY_PROMPT: ClassVar[str] = None
    SECONDARY_PROMPT: ClassVar[str] = None
    ERROR_PROMPT: ClassVar[str] = None

    def __init__(self) -> None:
        """Class initializer for the REPL."""
        self.config: Config = Config()
        Repl.setConstants()
        self.init()

    @classmethod
    def setConstants(cls) -> None:
        FileIO.setConstants(Config.data.get('file', {}))

        app_config: dict = Config.data.get('application', {})
        cls.AUTHOR = app_config.get('author', "HeyheyEason")
        cls.VERSION = app_config.get('version', [ 1, 0, 0 ])

        repl_config: dict = Config.data.get('repl', {})
        Color.setColorEnabled(repl_config.get('use-colored-terminal-text', True))
        cls.INDENT_STEP = repl_config.get('indent-step', 4)
        cls.PRIMARY_PROMPT = f"{Color.GREEN}{repl_config.get('prompts', {}).get('primary', ">>> ")}{Color.RESET}"
        cls.SECONDARY_PROMPT = f"{Color.BLUE}{repl_config.get('prompts', {}).get('secondary', "... ")}{Color.RESET}"
        cls.ERROR_PROMPT = f"{Color.RED}{repl_config.get('prompts', {}).get('error', "!!! ")}{Color.RESET}"

    def init(self) -> None:
        """Initialize the REPL environment."""
        self.repl_dict: dict[str, object] = {}
        self.final_script: str = ""
        self.indent_level: int = 0
        self.file_io: FileIO = FileIO()
        self.writing: bool = False
        self.reading: bool = False
        self.running: bool = True
        self.input_state: InputState = InputState.SINGLE_LINE

    @staticmethod
    def clearScreen() -> None:
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    @classmethod
    def printBanner(cls) -> None:
        """Print the REPL banner."""
        print(f"{Color.YELLOW}HeyheyEason PyREPL version {cls.VERSION[0]}.{cls.VERSION[1]}.{cls.VERSION[2]}{Color.RESET}")
        print(f"{Color.MAGENTA}Platform: Python {platform.python_version()} on {platform.system()} {platform.release()}{Color.RESET}")

    @classmethod
    def printVersion(cls) -> None:
        """Print the REPL Version."""
        print(f"{Color.MAGENTA}Version: {cls.VERSION[0]}.{cls.VERSION[1]}.{cls.VERSION[2]}{Color.RESET}")

    @classmethod
    def printCredits(cls) -> None:
        """Print the REPL credits."""
        print(f"{Color.MAGENTA}Created by {cls.AUTHOR}, all rights reserved.{Color.RESET}")

    def handleTermination(self) -> None:
        """Handle termination caused by the user."""
        self.running = False
        self.file_io.closeFile()
        print(f"{Color.RED}PyREPL stopped running due to the user's code.")
        print("Please restart to continue to use.")
        input(f"{Color.CYAN}Press Enter to exit...{Color.RESET}")

    def printDictionary(self) -> None:
        """Print the REPL dictionary to look up for names."""
        print(self.repl_dict)
        print()

    def resetEnvironment(self) -> None:
        """Reset the REPL environment and the file status except modules."""
        Repl.clearScreen()
        Repl.setConstants()
        self.init()
        Repl.printBanner()
        self.file_io.closeFile()
        print(f"{Color.CYAN}Note: PyREPL cannot really cancel importing modules.{Color.RESET}")

    # TODO: Implement the command for entering config editor.
    def processInternalCommand(self, line: str) -> bool:
        """Process internal REPL commands."""
        if line.lower() in ("exit", "quit"):
            self.running = False
            return True
        elif line.lower() == "clear":
            Repl.clearScreen()
            return True
        elif line.lower() == "dictionary":
            self.printDictionary()
            return True
        elif line.lower() == "reset":
            self.resetEnvironment()
            return True
        elif line.lower().startswith("help"):
            help_command: list[str] = line.split(" ")
            FileIO.getHelp(help_command[len(help_command) - 1])
            return True
        elif line.lower().startswith(("write", "append", "read", "delete")):
            edit_command = line.split(" ")

            if len(edit_command) < 2:
                print(f"{Color.RED}PyREPL Error: Missing file name for the command.{Color.RESET}\n")
                return True

            if not self.file_io.openFile(edit_command[0].lower(), edit_command[1].replace('"', '')):
                return True

            if edit_command[0] in ("write", "append"):
                self.writing = True
            elif edit_command[0] == "read":
                self.reading = True

            return True
        elif line.lower() == "save":
            if self.writing:
                self.file_io.closeFile()
                self.writing = False
                print(f"{Color.CYAN}File saved successfully.{Color.RESET}\n")
                return True
            else:
                print(f"{Color.RED}PyREPL Error: No file is currently being written to.{Color.RESET}\n")
                return True
        elif line.lower() == "config":
            user_decision: str = input(f"{Color.CYAN}Note: PyREPL will automatically reset after you enter the config editor. Are you sure to continue? (Y/N) {Color.RESET}")
            
            if user_decision.lower() == 'y':
                self.file_io.closeFile()
                Repl.clearScreen()
                self.config.runConsole()
                self.resetEnvironment()

            return True
        else:
            return False

    def resetStatus(self) -> None:
        """Reset the status when the code is executed or an exception occurred."""
        self.input_state = InputState.SINGLE_LINE
        self.final_script = ""
        self.indent_level = 0

    def run(self) -> None:
        """Run the REPL loop."""
        Repl.clearScreen()
        Repl.printBanner()

        while self.running:
            current_indent_str: str = " " * (self.indent_level * Repl.INDENT_STEP)
            prompt: str = Repl.PRIMARY_PROMPT if (self.indent_level <= 0 and self.input_state == InputState.SINGLE_LINE) else Repl.SECONDARY_PROMPT

            try:
                from_file: bool = False

                if self.reading:
                    from_file = True

                    while True:
                        line: str = self.file_io.read()

                        if not line:
                            self.file_io.closeFile()
                            break

                        self.final_script += line + "\n"
                        print(f"{Repl.SECONDARY_PROMPT}{line}")

                    self.reading = False
                    input(f"{Color.CYAN}Press Enter to finish reading the file...{Color.RESET}")
                else:
                    line: str = input(f"{prompt}{current_indent_str}").strip()

                if not self.final_script and self.processInternalCommand(line):
                    continue
                else:
                    if from_file:
                        code_obj: CodeType = compile(self.final_script, "<stdin>", "exec")
                    elif not line and self.final_script:
                        self.indent_level = max(0, self.indent_level - 1)
                    else:
                        self.final_script += current_indent_str + line + "\n"

                        # Special handling for unfinished multiline brackets
                        if line.endswith(('(', '[', '{')):
                            raise IndentationError

                        code_obj: CodeType = compile(self.final_script, "<stdin>", "exec")
                
                    if self.indent_level == 0 and self.final_script and self.input_state == InputState.MULTI_LINE:
                        self.input_state = InputState.AWAITING_MORE
                    elif self.indent_level == 0 and self.final_script and self.input_state != InputState.MULTI_LINE:
                        if self.writing:
                            if not self.file_io.write(self.final_script.rstrip()):
                                print(f"{Color.RED}PyREPL Error: Failed to write to file.{Color.RESET}\n")
                        else:
                            exec(code_obj, self.repl_dict)
                            print()

                        self.final_script = ""
                        self.input_state = InputState.SINGLE_LINE
            except IndentationError as e:
                # File input and explicit raise should not prompt for more input
                if from_file or "raise IndentationError" in self.final_script:
                    print(f"{Repl.ERROR_PROMPT}{Color.RED}{type(e).__name__}: {e}{Color.RESET}\n")
                    self.resetStatus()
                else:
                    self.input_state = InputState.MULTI_LINE
                    self.indent_level += 1
            except SyntaxError as e:
                # Check for incomplete brackets
                if ("'('" in str(e) or "'['" in str(e) or "'{'" in str(e)) and self.input_state == InputState.MULTI_LINE:
                    continue
                else:
                    print(f"{Repl.ERROR_PROMPT}{Color.RED}{type(e).__name__}: {e}{Color.RESET}\n")
                    self.resetStatus()
            except Exception as e:
                print(f"{Repl.ERROR_PROMPT}{Color.RED}{type(e).__name__}: {e}{Color.RESET}\n")
                self.resetStatus()
            except KeyboardInterrupt:
                print(f"{Color.CYAN}\nThe current input has been cancelled.{Color.RESET}\n")
                self.resetStatus()
