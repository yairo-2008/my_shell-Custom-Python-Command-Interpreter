# my_shell-Custom-Python-Command-Interpreter
A lightweight, functional command-line interface (Shell) built in Python that emulates Windows CMD behavior. This project demonstrates core operating system concepts, including process management, environment variable handling, and I/O redirection.

🚀 Features
Internal Commands: Native implementation of essential commands like CD, DIR, SET, TYPE, REN, CLS, and TIME.

I/O Redirection: Supports standard output redirection (>) and input redirection (<) to interact with files.

Piping: Implements process communication using the pipe (|) operator to chain multiple commands.

External Command Execution: Ability to execute external .exe files and system-wide commands via subprocess management.

Environment Management: View and modify session environment variables dynamically.

🛠️ Technical Highlights
Subprocess Management: Utilizes the subprocess module for process creation and synchronization.

File System Interaction: Deep integration with the os and glob modules for robust directory navigation and file manipulation.

Error Handling: Implements custom error messages for common CLI issues like "Path not found" or "Access denied".
