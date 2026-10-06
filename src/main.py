import os
import sys
import socket
import getpass
import shlex
import argparse


def get_prompt(vfs_path: str) -> str:
    user = getpass.getuser()
    host = socket.gethostname()
    return f"{user}@{host}:{vfs_path}$ "


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


def execute_script(script_path: str, vfs_path: str, debug: bool = False):
    if not os.path.isfile(script_path):
        print(f"Ошибка: файл скрипта '{script_path}' не найден.", file=sys.stderr)
        return False
    print(f"=== Выполнение стартового скрипта: {script_path} ===")
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"Ошибка чтения скрипта: {e}", file=sys.stderr)
        return False

    error_count = 0
    for line_num, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        prompt = get_prompt(vfs_path)
        print(f"{prompt}{line}")

        try:
            parts = shlex.split(line)
        except ValueError as e:
            print(f"Ошибка разбора строки {line_num}: {e}")
            error_count += 1
            continue

        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]
        handler = COMMANDS.get(cmd)
        if handler is None:
            print(f"Ошибка: неизвестная команда '{cmd}'")
            error_count += 1
            continue

        try:
            handler(args)
        except ValueError as e:
            print(f"Ошибка: {e}")
            error_count += 1
        except SystemExit:
            break
        except Exception as e:
            print(f"Ошибка выполнения: {e}")
            error_count += 1
    print(f"=== Скрипт завершён. Ошибочных строк: {error_count} ===")
    return error_count == 0


def run_interactive(vfs_path: str):
    print("Введите команду. Для выхода используйте exit.")
    while True:
        try:
            line = input(get_prompt(vfs_path))
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки UNIX-подобной ОС (Вариант №18, этап 2)."
    )
    parser.add_argument(
        "--vfs",
        type=str,
        default="myvfs",
        help="Путь к физическому расположению VFS.",
    )
    parser.add_argument(
        "--startup",
        type=str,
        default=None,
        help="Путь к стартовому скрипту для выполнения.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Вывести отладочную информацию о параметрах запуска.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("=== Параметры запуска ===")
    print(f"VFS: {args.vfs}")
    print(f"Startup script: {args.startup}")
    print("=========================")

    if args.startup:
        success = execute_script(args.startup, args.vfs, debug=args.debug)
        if not success:
            print("Скрипт завершился с ошибками.", file=sys.stderr)
            sys.exit(1)
    else:
        run_interactive(args.vfs)


if __name__ == "__main__":
    main()