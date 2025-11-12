# HeyheyEason PyREPL

[![Version](https://img.shields.io/badge/Version-2.1.3-blue.svg)](https://github.com/HeyheyEason/PyREPL/)
[![Python](https://img.shields.io/badge/Python-3.13+-informational.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.txt)

A **lightweight, feature-enhanced Python REPL environment** implemented purely with native Python logic. **PyREPL** is designed to provide an **efficient and practical interactive programming experience**, particularly well-suited for **script management and rapid code testing.**

---

# ✨ Project Features and Technical Highlights

PyREPL's design philosophy is to **replicate standard REPL behavior using pure logic** while integrating practical internal commands.

### 1. Core REPL Mechanism (Pure Logic Implementation)

* **Zero External Dependencies:** It does not rely on the `code` or `readline` modules from the Python standard library; all core REPL behaviors are implemented using custom logic.

* **Multi-line Code Block Handling:** Ingeniously utilizes the `try...except IndentationError` capture mechanism to accurately determine if multi-line input (such as `if` or `def` statements) has concluded, perfectly simulating the behavior of the native Python REPL.

* **Namespace Persistence:** By executing the code within a persistent dictionary namespace, it ensures that variables and functions are tracked and available throughout the entire session.

### 2. Original File I/O System (FileIO)

A powerful set of built-in file operation commands allows you to manage code scripts without exiting the REPL.

* **File Commands:** Supports `write` (overwrite/create), `append`, `read` (read and execute), `delete`, and `save` file operations.

* **Safety Mechanism:** Employs a state machine design to prevent opening or corrupting another file while one file operation is in progress.

---

### 3. Smart Help and Deployment Optimization

* **Smart Help System:**
    * For internal PyREPL topics (`help intro`), a local manual is displayed.
    * For keywords not on the internal list (`help list`), it **automatically navigates** to the **official documentation search page** for the current Python version via a web browser.
* **Lightweight Packaging Solution:** This design successfully bypasses the issue of missing documentation functionality when packaging into an executable—a problem often caused by the difficulty of including the bulky `pydoc` module—thereby maintaining the executable's lightweight nature and complete functionality.

---

## 🚀 How to Install and Run

### Prerequisites

* Python 3.13 or newer (**Important:** The project's `PYTHON_VERSION_INFO` dynamically retrieves online documentation based on your Python version.)

### Running from Source Code

1.  **Clone the Project:**
    ```bash
    git clone [https://github.com/HeyheyEason/PyREPL.git](https://github.com/HeyheyEason/PyREPL.git)
    cd PyREPL
    ```
2.  **Run the Program:**
    ```bash
    python "HeyheyEason PyREPL/src/main.py"
    ```

### Standalone Executable (Frozen Build)

* The [GitHub dist folder](https://github.com/HeyheyEason/PyREPL/tree/master/HeyheyEason%20PyREPL/dist) provides currently supported, pre-compiled executables.

---

### PyREPL Standalone (Executable) Version Support

The following table details the Python versions corresponding to the various supported releases of the PyREPL standalone executable:

| PyREPL Executable Version | Corresponding Python Version |
| :------------------------ | :--------------------------- |
| 1.4.3                     | 3.13.0                       |
| 1.5.2                     | 3.13.2                       |
| 2.0.4                     | 3.13.8                       |
| 2.1.2                     | 3.13.8                       |

---

### 📄 Further Information

For further usage instructions, please refer to the relevant documentation located in the project's `data/documents` folder.

This project is released under the **MIT License**. Please consult the [LICENSE](LICENSE.txt) file for full details.
