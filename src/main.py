import os
import sys
import socket
import getpass
import shlex

def get_prompt():
    user = getpass.getuser()
    host = socket.gethostname()
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]
    return f"{user}@{host}:{cwd}$ "


def cmd_ls(args):
    print(f"ls: {args}")

def cmd_cd(args):
    if len(args) != 1:
        raise ValueError("cd: требуется ровно один аргумент")
    print(f"cd: {args}")

def cmd_exit(args):
    if args:
        raise ValueError("exit: не принимает аргументов")
    print("Выход.")
    sys.exit(0)

COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}

def main():
    print("Введите команду. Для выхода используйте exit.")

    while True:
        try:
            line = input(get_prompt())
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break

        line = line.strip()
        if not line:
            continue

        try:
            parts = shlex.split(line)
        except ValueError as e:
            print(f"Ошибка разбора: {e}")
            continue

        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        handler = COMMANDS.get(cmd)
        if handler is None:
            print(f"Ошибка: неизвестная команда '{cmd}'")
            continue

        try:
            handler(args)
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Ошибка выполнения: {e}")

if __name__ == "__main__":
    main()
