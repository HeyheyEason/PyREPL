"""
==============================================================
File Information
    - Filename: repl_error.py
    - Project: HeyheyEason PyREPL
    - Module: system.repl_error
    - Description: File defining Config class and the editor.
    - Last Modified: 2025-11-22
==============================================================
"""

import sys
import json
from pathlib import Path
from typing import ClassVar, Any, Optional, Union
from utilities import Color
from .repl_error import ReplError

class Config:
    """Class for configuration of the REPL."""

    PROJECT_DIR: ClassVar[Path] = Path(sys.executable).resolve().parent.parent.parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent.parent.parent
    CONFIG_DIR: ClassVar[Path] = PROJECT_DIR / "data" / "assets" / "config.json"
    __DISABLE_EDITOR: ClassVar[bool] = None
    data: ClassVar[dict[str, Any]] = {}
    
    def __init__(self) -> None:
        """Initializer for Config class."""
        self.is_dirty: bool = False
        Config.loadConfig()
    
    @classmethod
    def loadConfig(cls) -> None:
        """Parse config.json file."""
        if Path.exists(cls.CONFIG_DIR):
            try:
                with open(cls.CONFIG_DIR, "r", encoding="utf-8") as file:
                    cls.data = json.load(file)
                    cls.__DISABLE_EDITOR = cls.data.get('disable-config-editor', False)
            except json.JSONDecodeError as e:
                raise ReplError("Config file decoding failed.", 1, str(e))
            except Exception as e:
                raise ReplError("Unknown exception occurred to the config file.", 2, str(e))
        else:
            print(f"{Color.RED}Config file not found at '{Config.CONFIG_DIR}'. Using default config.{Color.RESET}")


    def save(self) -> None:
        """Save the config to the config.json file."""
        try:
            with open(Config.CONFIG_DIR, "w", encoding="utf-8") as file:
                json.dump(Config.data, file, indent=4, ensure_ascii=False)
            self.is_dirty = False
        except Exception as e:
            raise ReplError("File 'config.json' is missing.", 3, str(e))

    # --- Path Resolution & Value Conversion ---

    def resolvePath(self, path: list[str], create_if_not_exists: bool = False) -> tuple[Optional[Union[dict, list]], Optional[Union[str, int]], Optional[Any]]:
        """Resolve the path and return parent node, final key/index, and final value."""
        if not path:
            return None, None, Config.data

        current: dict[str, Any] = Config.data
        parent: Optional[dict[str, Any]] = None
        final_key_or_index: Optional[Union[str, int]] = None

        for i, segment in enumerate(path):
            parent = current

            if isinstance(current, dict):
                final_key_or_index = segment

                if segment in current:
                    current: dict[str, Any] = current[segment]
                elif create_if_not_exists and i == len(path) - 1:
                    return parent, final_key_or_index, None
                else:
                    return None, None, None
            elif isinstance(current, list):
                try:
                    index: int = int(segment)
                    final_key_or_index = index

                    if 0 <= index < len(current):
                        current = current[index]
                    else:
                        return None, None, None
                except ValueError:
                    return None, None, None
            else:
                return None, None, None

        return parent, final_key_or_index, current

    def getValue(self, path: list[str]) -> Any:
        """Get value according to the list of keys/indexes."""
        if not path:
            return Config.data

        _, _, value = self.resolvePath(path)
        return value

    def convertValue(self, value_str: str) -> Any:
        """Attempt to convert value into a proper type."""
        value_str: str = value_str.strip()

        if value_str.lower() in ("true", "false"):
            return value_str.lower() == "true"

        if value_str.lower() in ("null", "none"):
            return None

        try:
            if '.' in value_str:
                return float(value_str)
            else:
                return int(value_str)
        except ValueError:
            pass

        if value_str.startswith(('{', '[')):
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                pass

        return value_str

    # --- Core CRUD Operations ---

    def setValue(self, path: list[str], value_str: str) -> tuple[bool, str]:
        """Set the value in path and execute type conversion."""
        if not path:
            return False, f"{Color.RED}Cannot modify the value of root.{Color.RESET}"

        parent, key_or_index, _ = self.resolvePath(path, True)
        new_value: Any = self.convertValue(value_str)

        if parent is None:
            return False, f"{Color.RED}Invalid path: {'/'.join(path)}{Color.RESET}"

        if isinstance(parent, dict) and isinstance(key_or_index, str):
            parent[key_or_index] = new_value
            self.is_dirty = True
            return True, f"{Color.GREEN}Key '{key_or_index}' value set to {new_value} ({type(new_value).__name__}).{Color.RESET}"
        elif isinstance(parent, list) and isinstance(key_or_index, int):
            if 0 <= key_or_index < len(parent):
                parent[key_or_index] = new_value
                self.is_dirty = True
                return True, f"{Color.GREEN}Index '{key_or_index}' value set to {new_value} ({type(new_value).__name__}).{Color.RESET}"
            else:
                return False, f"{Color.RED}Index '{key_or_index}' is out of range.{Color.RESET}"
        else:
            return False, f"{Color.RED}Cannot set value at current position.{Color.RESET}"

    def deleteValue(self, path: list[str]) -> tuple[bool, str]:
        """Delete assigned key or index."""
        if not path:
            return False, "Cannot delete the root."
            
        parent, key_or_index, _ = self.resolvePath(path)
        
        if parent is None or key_or_index is None:
            return False, f"Path not found: {'/'.join(path)}"

        if isinstance(parent, dict) and isinstance(key_or_index, str):
            del parent[key_or_index]
            self.is_dirty = True
            return True, f"{Color.GREEN}Key '{key_or_index}' has been deleted.{Color.RESET}"
        elif isinstance(parent, list) and isinstance(key_or_index, int):
            if 0 <= key_or_index < len(parent):
                parent.pop(key_or_index)
                self.is_dirty = True
                return True, f"{Color.GREEN}Index '{key_or_index}' has been deleted.{Color.RESET}"
            else:
                return False, f"{Color.RED}Index '{key_or_index}' is out of range.{Color.RESET}"
        
        return False, f"{Color.RED}Cannot delete value based on this type.{Color.RESET}"

    # --- List Operations ---

    def appendValue(self, path: list[str], value_str: str) -> tuple[bool, str]:
        """Append new elements to the back of the list"""
        current_value: Any = self.getValue(path)
        
        if not isinstance(current_value, list):
            return False, f"{Color.RED}Operation failed: path '/{'/' .join(path)}' didn't point to a list. ({type(current_value).__name__}){Color.RESET}"

        new_value: Any = self.convertValue(value_str)
        current_value.append(new_value)
        self.is_dirty = True
        return True, f"{Color.GREEN}New element appended: {new_value} ({type(new_value).__name__}){Color.RESET}"

    def insertValue(self, path: list[str], index_str: str, value_str: str) -> tuple[bool, str]:
        """Insert value to the assigned index."""
        current_value: Any = self.getValue(path)

        if not isinstance(current_value, list):
            return False, f"{Color.RED}Operation failed: path '/{'/' .join(path)}' didn't point to a list. ({type(current_value).__name__}){Color.RESET}"
        
        try:
            index = int(index_str)
        except ValueError:
            return False, f"{Color.RED}Index '{index_str}' must be a valid integer.{Color.RESET}"

        if index < 0 or index > len(current_value):
            return False, f"{Color.RED}Index '{index}' is out of range. Valid range: 0 to {len(current_value)}.{Color.RESET}"

        new_value: Any = self.convertValue(value_str)
        current_value.insert(index, new_value)
        self.is_dirty = True
        return True, f"{Color.GREEN}New element inserted at index '{index}': {new_value} ({type(new_value).__name__}){Color.RESET}"

    # --- Console Utilities (for Refactoring) ---

    def parseConsolePath(self, input_str: str) -> list[str]:
        """Parse the path into a list."""
        if not input_str:
            return []
        
        temp_str: str = input_str.replace('[', '.').replace(']', '.')
        segments: list[str] = [s for s in temp_str.split('.') if s]
        return segments
    
    # ----------------------------------------------------
    # Refactoring: Separated Command Handlers
    # ----------------------------------------------------
    
    def _handleShowHelp(self):
        """Display the help message."""
        help_text: str = \
            "\n--- PyREPL Config Editor Commands ---\n" + \
            "[path]=[value]      : Set value at path. Supports numbers, booleans, JSON structures, and null/None.\n" + \
            "[path]              : Navigate to sub-key or list index (e.g., 'database' or '0').\n" + \
            "show [path]         : Display value at current or specified path.\n" + \
            "delete [path]       : Delete key or index at specified path.\n" + \
            "append [value]      : Append an element to the list at the current path. (Must be a list)\n" + \
            "insert [idx] [value]: Insert an element at the specified index of the list at the current path. (Must be a list)\n" + \
            "/                   : Go back to the root directory.\n" + \
            "..                  : Go back to the upper level.\n" + \
            "save                : Save changes to file and quit the editor.\n" + \
            "Ctrl+C              : Quit without saving (reverts config).\n" + \
            "-------------------------------------\n"
                         
        print(help_text)

    def _handleSetCommand(self, user_input: str, current_path: list[str]):
        """Handle path=value setting command."""
        path_str, value_str = user_input.split('=', 1)
        path_str = path_str.strip()
        value_str = value_str.strip()
        
        relative_path: list[str] = self.parseConsolePath(path_str)
        new_path: list[str] = current_path + relative_path
        
        _, message = self.setValue(new_path, value_str)
        print(message)

    def _handleShowCommand(self, parts: list[str], current_path: list[str]):
        """Handle the 'show' command."""
        path_str: Optional[str] = parts[1].strip() if len(parts) > 1 else None
        
        if path_str:
            relative_path: list[str] = self.parseConsolePath(path_str)
            target_path: list[str] = current_path + relative_path
        else:
            target_path = current_path

        value: Any = self.getValue(target_path)
        self._showValue(value, target_path)

    def _handleDeleteCommand(self, parts: list[str], current_path: list[str]):
        """Handle the 'delete' command."""
        if len(parts) < 2:
            print(f"{Color.RED}Missing key target. Example: delete key_to_delete{Color.RESET}")
            return
            
        path_str: str = parts[1].strip()
        relative_path: list[str] = self.parseConsolePath(path_str)
        target_path: list[str] = current_path + relative_path
        
        _, message = self.deleteValue(target_path)
        print(message)

    def _handleListInsertCommand(self, command: str, parts: list[str], current_path: list[str]):
        """Handle 'append' and 'insert' commands."""
        if command == 'append':
            if len(parts) < 2:
                print(f"{Color.RED}Missing element. Example: append \"new_item\"{Color.RESET}")
                return
            value_str: str = parts[1].strip()
            _, message = self.appendValue(current_path, value_str)
        
        elif command == 'insert':
            if len(parts) < 3:
                print(f"{Color.RED}Missing index or value. Example: insert 0 \"first\"{Color.RESET}")
                return
            index_str: str = parts[1].strip()
            value_str: str = parts[2].strip()
            _, message = self.insertValue(current_path, index_str, value_str)
        
        print(message)

    def _handleNavigation(self, path_str: str, current_path: list[str]) -> bool:
        """Handle path-only input for navigation. Returns True if navigated."""
        relative_path: list[str] = self.parseConsolePath(path_str)

        if not relative_path:
            print(f"{Color.RED}Invalid command or path.{Color.RESET}")
            return False
        
        if len(relative_path) == 1:
            key_or_index: str = relative_path[0]
            target_path: list[str] = current_path + [key_or_index]
            target_value: Any = self.getValue(target_path)
            current_value: Any = self.getValue(current_path)
            
            is_current_list: bool = isinstance(current_value, list)
            is_current_dict_or_root: bool = isinstance(current_value, dict) or not current_path

            if is_current_list:
                try:
                    index: int = int(key_or_index)
                    if 0 <= index < len(current_value):
                        if isinstance(target_value, (dict, list)):
                            current_path.append(key_or_index)
                            return True
                        elif target_value is not None:
                            print(f"{Color.RED}Index '{index}' value type: {type(target_value).__name__}. Not a container.")
                            print(f"Use 'show {index}' to view or '{index}=[value]' to modify.\n{Color.RESET}")
                        else:
                            print(f"{Color.RED}Index '{index}' exists but value is null.\n{Color.RESET}")
                    else:
                        print(f"{Color.RED}Index '{index}' is out of range.\n{Color.RESET}")
                        
                except ValueError:
                    print(f"{Color.RED}Currently in a list, please use a numerical index for navigation.\n{Color.RESET}")
            
            elif is_current_dict_or_root:
                if isinstance(target_value, (dict, list)):
                    current_path.append(key_or_index)
                    return True
                elif target_value is not None:
                    print(f"{Color.RED}Key '{key_or_index}' value type: {type(target_value).__name__}. Not a container.")
                    print(f"Use 'show {key_or_index}' to view or '{key_or_index}=[value]' to modify.\n{Color.RESET}")
                else:
                    print(f"{Color.RED}Key '{key_or_index}' not found.\n{Color.RESET}")
            
            else:
                print(f"{Color.RED}Cannot navigate inside a '{type(current_value).__name__}' type. Use '..' to go back to the upper level.\n{Color.RESET}")            
            return False
        else:
            print(f"{Color.RED}Cannot navigate multiple levels at once. Please enter a single key or index.{Color.RESET}")
            return False
        
    def _showValue(self, value: Any, path: list[str]):
        """Formatted output of the config."""
        path_display: str = '/' + '/'.join(path) if path else '/'
        print(f"\n--- Current path ({path_display}) contents ---")
        
        if isinstance(value, (dict, list)):
            print(json.dumps(value, indent=4, ensure_ascii=False))
        elif value is None:
            print("Value: null (NoneType)")
        else:
            print(f"Value: {value} ({type(value).__name__})")
            
        print("--- End ---\n")

    # ----------------------------------------------------
    # Main Console Loop
    # ----------------------------------------------------

    def runConsole(self) -> None:
        """The main loop of config editor console."""
        if Config.__DISABLE_EDITOR:
            print(f"{Color.YELLOW}PyREPL Config Editor Console: TERMINATED")
            print(f"{Color.RED}The config editor has been disabled by config.json. Please turn to your JSON editor.")
            print(f"{Color.CYAN}Note: Set 'disable-config-editor' to false if you want to activate the editor.")
            input(f"Press Enter to continue...{Color.RESET}")
            return

        current_path: list[str] = []  # Define current path

        def getPrompt():
            """Get Console prompt."""
            path_str: str = '/' + '/'.join(current_path) if current_path else '/'
            dirty_flag: str = f"{Color.BLUE}*{Color.MAGENTA}" if self.is_dirty else ""
            return f"{Color.MAGENTA}config{dirty_flag}:{path_str} > {Color.RESET}"

        print(f"{Color.YELLOW}You are in PyREPL Config Editor Console. Enter 'help' for commands.{Color.RESET}")
        print(f"{Color.CYAN}Note: use 'save' to save and quit. Use Ctrl+C to quit without saving (revert).{Color.RESET}")

        while True:
            try:
                user_input: str = input(getPrompt()).strip()
            except EOFError:
                print(f"{Color.RED}Error: Please use 'save' or Ctrl+C to quit.{Color.RESET}")
                continue
            except KeyboardInterrupt:
                Config.loadConfig() # Revert
                return

            if not user_input:
                continue
            
            parts: list[str] = user_input.split(maxsplit=2)
            command: str = parts[0].lower()
            
            # 1. Handle primary commands (save, help)
            if command == 'save':
                self.save()
                break 
            
            elif command == 'help':
                self._handleShowHelp()
                continue
                
            # 2. Handle simple navigation (/, ..)
            elif command == '/':
                current_path = []
                continue
            elif command == '..':
                if current_path:
                    current_path.pop()
                else:
                    print(f"{Color.CYAN}Already at the root.\n{Color.RESET}")
                continue

            # 3. Handle list modification (append, insert)
            elif command in ('append', 'insert'):
                self._handleListInsertCommand(command, parts, current_path)
                continue

            # 4. Handle CRUD commands (show, delete)
            elif command == 'show':
                self._handleShowCommand(parts, current_path)
                continue

            elif command == 'delete':
                self._handleDeleteCommand(parts, current_path)
                continue

            # 5. Handle setting value ([path]=[value])
            elif '=' in user_input:
                self._handleSetCommand(user_input, current_path)

            # 6. Handle single path navigation (implicitly changes current_path)
            else:
                path_str = user_input.strip()
                self._handleNavigation(path_str, current_path)