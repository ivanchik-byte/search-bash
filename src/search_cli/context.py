import sys
from pathlib import Path

MAX_STDIN_BYTES = 2 * 1024 * 1024
MAX_FILE_BYTES = 1 * 1024 * 1024

IGNORED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "venv", ".venv", "env",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".idea", ".vscode",
    "build", "dist", "target", ".cache", ".next", ".nuxt", "vendor"
}


def read_piped_stdin() -> str:
    if sys.stdin.isatty():
        return ""
    try:
        raw_data = sys.stdin.buffer.read(MAX_STDIN_BYTES + 1)
        if len(raw_data) > MAX_STDIN_BYTES:
            print(f"[-] Warning: stdin exceeded {MAX_STDIN_BYTES // 1024 // 1024}MB and was truncated.", file=sys.stderr)
            raw_data = raw_data[:MAX_STDIN_BYTES]
        return raw_data.decode("utf-8", errors="replace").strip()
    except Exception as e:
        print(f"[-] Warning: failed to read stdin: {e}", file=sys.stderr)
        return ""


def read_file_context(file_path: str) -> str:
    p = Path(file_path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not p.is_file():
        raise ValueError(f"Path is not a regular file: {file_path}")

    size = p.stat().st_size
    if size > MAX_FILE_BYTES:
        raise ValueError(f"File too large ({size // 1024}KB, max {MAX_FILE_BYTES // 1024}KB): {file_path}")

    try:
        content = p.read_text(encoding="utf-8", errors="replace")
        return f"File: {p.name}\nPath: {p}\n```\n{content}\n```"
    except Exception as e:
        raise RuntimeError(f"Could not read file {file_path}: {e}")


def scan_directory(dir_path: str, max_depth: int = 3, max_files: int = 150) -> str:
    root = Path(dir_path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    if not root.is_dir():
        raise ValueError(f"Path is not a directory: {dir_path}")

    tree_lines = [f"{root.name}/"]
    file_count = 0
    important_files = []

    def walk(current: Path, prefix: str, depth: int):
        nonlocal file_count
        if depth > max_depth or file_count >= max_files:
            return

        try:
            entries = sorted(list(current.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            return

        visible_entries = [e for e in entries if e.name not in IGNORED_DIRS and not e.name.startswith(".")]

        for idx, entry in enumerate(visible_entries):
            if file_count >= max_files:
                tree_lines.append(f"{prefix}... (file limit reached)")
                break

            is_last = idx == len(visible_entries) - 1
            connector = "\\-- " if is_last else "|-- "
            sub_prefix = "    " if is_last else "|   "

            if entry.is_dir():
                tree_lines.append(f"{prefix}{connector}{entry.name}/")
                walk(entry, prefix + sub_prefix, depth + 1)
            else:
                file_count += 1
                tree_lines.append(f"{prefix}{connector}{entry.name}")
                if entry.name.lower() in {
                    "readme.md", "pyproject.toml", "package.json", "cargo.toml",
                    "go.mod", "dockerfile", "docker-compose.yml", "makefile"
                }:
                    important_files.append(entry)

    walk(root, "", 1)

    result = [
        f"Directory Tree for {root}:",
        "\n".join(tree_lines),
        f"\nTotal files indexed: {file_count}"
    ]

    for imp in important_files[:2]:
        try:
            content = imp.read_text(encoding="utf-8", errors="replace")[:1500]
            result.append(f"\n--- Preview of {imp.name} ---\n{content}")
        except Exception:
            pass

    return "\n".join(result)
