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


def _run_command(line: str) -> None:
    parts = shlex.split(line)
    if not parts:
        return
    cmd = parts[0]
    handler = COMMANDS.get(cmd)
    if handler is None:
        raise ValueError(f"неизвестная команда '{cmd}'")
    handler(parts[1:])


def _run_script_line(line: str, vfs_path: str) -> bool:
    prompt = get_prompt(vfs_path)
    print(f"{prompt}{line}")
    try:
        _run_command(line)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return False
    except Exception as exc:
        print(f"Ошибка выполнения: {exc}")
        return False
    return True


def execute_script(script_path: str, vfs_path: str) -> bool:
    if not os.path.isfile(script_path):
        print(f"Файл скрипта '{script_path}' не найден.",
              file=sys.stderr)
        return False

    print(f"=== Выполнение стартового скрипта: {script_path} ===")

    try:
        with open(script_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except OSError as exc:
        print(f"Ошибка чтения скрипта: {exc}", file=sys.stderr)
        return False

    error_count = 0
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith(("#", "//")):
            continue

        try:
            ok = _run_script_line(line, vfs_path)
        except SystemExit:
            break

        if not ok:
            error_count += 1

    print(f"=== Скрипт завершён. Ошибочных строк: {error_count} ===")
    return error_count == 0


def run_interactive(vfs_path: str) -> None:
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
            _run_command(line)
        except ValueError as exc:
            print(f"Ошибка: {exc}")
        except Exception as exc:
            print(f"Ошибка выполнения: {exc}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки UNIX-подобной ОС"
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


def main() -> None:
    args = parse_args()

    print("=== Параметры запуска ===")
    print(f"VFS: {args.vfs}")
    print(f"Startup script: {args.startup}")
    print("=========================")

    if args.startup:
        success = execute_script(args.startup, args.vfs)
        if not success:
            print("Скрипт завершился с ошибками.", file=sys.stderr)
            sys.exit(1)
    else:
        run_interactive(args.vfs)


if __name__ == "__main__":
    main()