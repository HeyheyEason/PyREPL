"""
==============================================================
File Information
    - Filename: repl.py
    - Project: HeyheyEason PyREPL
    - Module: core.repl
    - Description: The implementation of the REPL.
    - Last Modified: 2025-11-12
==============================================================
"""

import os
import platform
from types import CodeType
from .file_io import FileIO
from utilities import InputState, Color

class Repl:
    """Class representing the REPL environnemt."""

    # Define indentation step
    INDENT_STEP: int = 4

    # Define prompt strings with colors
    PRIMARY_PROMPT: str = f"{Color.GREEN}>>> {Color.RESET}"
    SECONDARY_PROMPT: str = f"{Color.BLUE}... {Color.RESET}"
    ERROR_PROMPT: str = f"{Color.RED}!!! {Color.RESET}"

    # Define REPL version
    VERSION: str = "2.1.2"

    def __init__(self) -> None:
        """Class initializer for the REPL."""
        self.init()

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
        print(f"{Color.YELLOW}HeyheyEason PyREPL version {cls.VERSION}{Color.RESET}")
        print(f"{Color.MAGENTA}Platform: Python {platform.python_version()} on {platform.system()} {platform.release()}{Color.RESET}")

    @classmethod
    def printVersion(cls) -> None:
        """Print the REPL Version."""
        print(f"{Color.MAGENTA}Version: {cls.VERSION}{Color.RESET}")

    @staticmethod
    def printCredits() -> None:
        """Print the REPL credits."""
        print(f"{Color.MAGENTA}Created by HeyheyEason, all rights reserved.{Color.RESET}")

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

    def resetEnvironment(self) -> None:
        """Reset the REPL environment except modules."""
        Repl.clearScreen()
        self.init()
        Repl.printBanner()
        print(f"{Color.CYAN}Note: PyREPL cannot really cancel importing modules.{Color.RESET}")

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
            self.file_io.getHelp(help_command[len(help_command) - 1])
            return True
        elif line.lower().startswith(("write", "append", "read", "delete")):
            edit_command = line.split(" ")

            if len(edit_command) < 2:
                print(f"{Color.RED}PyREPL Error: Missing file name for the command.{Color.RESET}")
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
                print(f"{Color.CYAN}File saved successfully.{Color.RESET}")
                return True
            else:
                print(f"{Color.RED}PyREPL Error: No file is currently being written to.{Color.RESET}")
                return True
        else:
            return False

    def run(self) -> None:
        """Run the REPL loop."""
        Repl.clearScreen()
        self.init()
        Repl.printBanner()

        while True:
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
                    if not self.running:
                        return
                    else:
                        continue
                else:
                    if from_file:
                        code_obj: CodeType = compile(self.final_script, "<stdin>", "exec")
                    elif not line and self.final_script:
                        self.indent_level = max(0, self.indent_level - 1)
                    else:
                        self.final_script += current_indent_str + line + "\n"
                        code_obj: CodeType = compile(self.final_script, "<stdin>", "exec")
                
                    if self.indent_level == 0 and self.final_script and self.input_state == InputState.MULTI_LINE:
                        self.input_state = InputState.AWAITING_MORE
                    elif self.indent_level == 0 and self.final_script and self.input_state != InputState.MULTI_LINE:
                        if self.writing:
                            if not self.file_io.write(self.final_script.rstrip()):
                                print(f"{Color.RED}PyREPL Error: Failed to write to file.{Color.RESET}")
                        else:
                            exec(code_obj, self.repl_dict)

                        self.final_script = ""
                        self.input_state = InputState.SINGLE_LINE
            except IndentationError:
                self.input_state = InputState.MULTI_LINE
                self.indent_level += 1
            except Exception as e:
                print(f"{Repl.ERROR_PROMPT}{Color.RED}{type(e).__name__}: {e}{Color.RESET}")
                self.input_state = InputState.SINGLE_LINE
                self.final_script = ""
                self.indent_level = 0