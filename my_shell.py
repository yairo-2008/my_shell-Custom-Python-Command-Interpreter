__author__ = 'Omer Yair'
import subprocess
import os
import datetime
from logging import exception
import glob

help_functions = {"CD":"Displays the name of or changes the current directory.",
                  "SET":"Displays, sets, or removes Windows environment variables.",
                  "EXIT":"Quits the my_shell program (command interpreter).",
                  "CLS":"Clears the screen.",
                  "DIR":"Displays a list of files and subdirectories in a directory.",
                  "TIME":"Displays or sets the system time.",
                  "TYPE":"Displays the contents of a text file.",
                  "REN":"Renames a file or files."}

internal_commands = ['CD','SET','EXIT','HELP','CLS','DIR','TIME','TYPE','REN']
my_path = [r"D:\סייבר\מערכות הפעלה\my_shell\Commands",]

def run_shell_functions():
    subprocess.run(args=r"cmd /c dir c:\windows")
    subprocess.run(args=[r"cmd /c dir c:\Program Files"], shell=True)
    subprocess.run(args=[r"cmd /c", "dir", r"c:\Program Files"], shell=True)
    #subprocess.run(args=[r"python", "example1.py"])
    os.getcwd()
    #os.chdir(r'C:\temp\folder2')
    print(os.getcwd())
    #subprocess.run(args=["python", "example1.py"], cwd=r'C:\temp\folder1')

def run_internal_commands(args):
    global help_functions
    if args[0] == 'EXIT':
        return -1
    elif args[0] == 'HELP':
        if len(args) > 3:
            print('Provides help information for Windows commands.\nHELP [command]\ncommand - displays help information on that command.')
        if len(args) > 1:
            if args[1] in help_functions:
                print(f'{args[1]} : {help_functions[args[1]]}')
            else:
                print('This command is not supported by the help utility.')
        else:
            print('For more information on a specific command, type HELP command-name')
            for k,v in help_functions.items():
                print(f'{k}:{v}')
    elif args[0] == 'CD':
        if len(args) == 1:
            print(os.getcwd())
        else:
            try:
                full_path = " ".join(args[1:])
                os.chdir(full_path)
            except FileNotFoundError:
                        print(f"The system cannot find the path specified.")
            except IndexError:
                print("needs a path!")
    elif args[0] == 'SET':
        if len(args) == 1:
            for key, value in os.environ.items():
                print(f'{key}={value}')
            return
        set_command = " ".join(args[1:])

        if '=' in set_command:
            key, value = set_command.split('=', 1)
            key = key.strip()
            value = value.strip()
            os.environ[key] = value
        else:
            try:
                print(f"{set_command}={os.environ[set_command]}")
            except KeyError:
                print(f"Environment variable '{set_command}' is not defined.")
    elif args[0] == 'CLS':
        os.system('cls')

    elif args[0] == 'DIR':
        path = os.getcwd()
        show_all = False
        recursive = False

        new_args = []
        for a in args[1:]:
            if a.upper() == "/A":
                show_all = True
            elif a.upper() == "/S":
                recursive = True
            else:
                new_args.append(a)

        if new_args:
            path = " ".join(new_args)

        if not os.path.exists(path):
            print(f"Error: The directory {path} does not exist.")
        elif not os.path.isdir(path):
            print(f"Error: {path} is not a directory.")
        else:
            def list_dir(current_path, prefix=""):
                try:
                    entries = os.listdir(current_path)
                except PermissionError:
                    print(f"Access denied: {current_path}")
                    return

                for entry in entries:
                    full_path = os.path.join(current_path, entry)
                    if not show_all and entry.startswith('.'):
                        continue
                    if os.path.isdir(full_path):
                        print(f"<DIR>\t{entry}")
                        if recursive:
                            list_dir(full_path, prefix + "  ")
                    else:
                        size = os.path.getsize(full_path)
                        print(f"{size} bytes\t{entry}")

            print(f"Directory of {path}\n")
            list_dir(path)

    elif args[0] == "TIME":
        print(f'The current time is:{datetime.datetime.now().strftime("%H:%M:%S.%f")}')
        new_time = input('Enter the new time:')
        if new_time=='':
            print('------------')
        else:
            try:
                os.system(f"time {new_time}")
            except exception:
                print('A required privilege is not held by the client.')

    elif args[0] == 'TYPE':
        if len(args) < 2:
            print("The syntax of the command is incorrect.\nUsage: TYPE filename")
        else:
            file_name = " ".join(args[1:])
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    print(f.read())
            except FileNotFoundError:
                print(f"The system cannot find the file specified: {file_name}")
            except PermissionError:
                print(f"Access is denied: {file_name}")
            except UnicodeDecodeError:
                print(f"{file_name} is not a text file.")
    elif args[0] == 'REN':
        if len(args) < 3:
            print("Asked REN [source] [destination] [/A] [/O]")
        else:
            source = args[1]
            destination = args[2]
            apply_all = False
            overwrite = False
            for a in args[3:]:
                if a.upper() == "/A":
                    apply_all = True
                elif a.upper() == "/O":
                    overwrite = True

            try:
                if apply_all:
                    for f in glob.glob(source):
                        new_name = destination
                        if overwrite or not os.path.exists(new_name):
                            os.rename(f, new_name)
                        else:
                            print(f"File exists: {new_name}, use /O to overwrite.")
                else:
                    if overwrite or not os.path.exists(destination):
                        os.rename(source, destination)
                    else:
                        print(f"File exists: {destination}, use /O to overwrite.")
            except FileNotFoundError:
                print(f"File not found: {source}")
            except PermissionError:
                print(f"Access denied: {source}")
            except Exception as e:
                print(f"Error: {e}")

def run_external_commands(args):
    global my_path
    params = [" ".join(args[1:])]

    for path in my_path:
        opt = os.path.join(path, args[0])
        if os.path.isfile(opt):
            subprocess.run(["python", opt] + params)
            return True
    return False

def run_cmd_command(args):
    cmd = args[0]
    params = args[1:]
    try:
        subprocess.run([r"cmd", "/c", cmd] + params, shell=True)
        return True
    except FileNotFoundError:
        print(f"Command not found: {cmd}")
        return False

def do_exe_files(args):
    try:
        if args:
            subprocess.run([args[0]] + args[:1], check=True)
            return True
        else:
            subprocess.run([args[0]], check=True)
            return True
    except Exception as error:
        print(f"error occurred: {error}")
        return False

def do_redirect(args):
    try:
        cmd = []
        stdin = None
        stdout = None

        if ">" in args:
            parts = " ".join(args).split(">")
            cmd = parts[0].strip().split()
            stdout_file = parts[1].strip()
            stdout = open(stdout_file, "w")
        elif "<" in args:
            parts = " ".join(args).split("<")
            cmd = parts[0].strip().split()
            stdin_file = parts[1].strip()
            stdin = open(stdin_file, "r")
        else:
            cmd = args
    except Exception as e:
        print(f'error:{e}')
    try:
        subprocess.run(cmd, stdin=stdin, stdout=stdout, shell=True)
    except Exception as e:
        print(f"Error running command with redirect: {e}")
    finally:
        if stdin:
            stdin.close()
        if stdout:
            stdout.close()

def do_pipe(args):
    if "|" not in args:
        print("No pipe found.")
        return

    left_cmd, right_cmd = " ".join(args).split("|", 1)
    left_args = left_cmd.strip().split()
    right_args = right_cmd.strip().split()

    try:
        p1 = subprocess.Popen(left_args, stdout=subprocess.PIPE, shell=True)
        p2 = subprocess.Popen(right_args, stdin=p1.stdout, stdout=subprocess.PIPE, shell=True)
        p1.stdout.close()
        output, _ = p2.communicate()
        print(output.decode())
    except Exception as e:
        print(f"Error in pipe: {e}")


def main():
    print('hi! Welcome to my_shell')
    user_name = input('write your name: ')
    while True:
        print('')
        command_input = input(f"{os.getcwd()}~{user_name}_my-shell>").strip()
        print('')
        args = command_input.split()
        if not command_input:
            continue

        if "|" in command_input:
            do_pipe(args)
            continue
        if ">" in command_input or "<" in command_input:
            do_redirect(args)
            continue
        args[0] = args[0].upper()
        if args[0] in internal_commands:
            if run_internal_commands(args) == -1:
                break
        elif run_external_commands(args):
            pass
        elif args[0].endswith(".EXE"):
            do_exe_files(args)
        elif run_cmd_command(args):
            pass
        else:
            print(f'{args[0]} is not recognized as an internal or external command.')

    print(f'Thanks for using my_shell by {__author__}')

if __name__ == '__main__':
    main()
