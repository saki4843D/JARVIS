"""Safe file operations for explicit JARVIS commands."""
from pathlib import Path
import os
import subprocess


ROOT = Path.home()


def _resolve(raw_path):
    candidate = Path(raw_path.strip().strip('"'))
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    return candidate.expanduser().resolve()


def _display(path):
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def handle(command):
    command = command.lower().strip()
    if command in {"list files", "show files", "list files here"}:
        entries = sorted(Path.cwd().iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
        if not entries:
            return "This folder is empty."
        preview = ", ".join(item.name for item in entries[:12])
        suffix = " and more" if len(entries) > 12 else ""
        return f"I found {len(entries)} items: {preview}{suffix}."

    for prefix in ("open file ", "open folder "):
        if command.startswith(prefix):
            path = _resolve(command.removeprefix(prefix))
            if not path.exists():
                return f"I couldn't find {_display(path)}."
            try:
                os.startfile(path)
                return f"Opening {_display(path)}."
            except OSError:
                return f"I couldn't open {_display(path)}."

    if command.startswith("show files in "):
        path = _resolve(command.removeprefix("show files in "))
        if not path.is_dir():
            return f"That folder does not exist: {_display(path)}."
        names = sorted(item.name for item in path.iterdir())[:12]
        return f"{_display(path)} contains: {', '.join(names) or 'no files'}."

    if command.startswith("delete file ") or command.startswith("delete folder "):
        path = _resolve(command.split(" ", 2)[2])
        if not path.exists():
            return f"I couldn't find {_display(path)}."
        return f"DELETE_CONFIRM:{path}"

    return None


def delete_path(raw_path):
    path = _resolve(raw_path)
    try:
        if path.is_dir():
            return "Folders require manual deletion to avoid removing nested data."
        path.unlink()
        return f"Deleted {_display(path)}."
    except OSError:
        return f"I couldn't delete {_display(path)}."
