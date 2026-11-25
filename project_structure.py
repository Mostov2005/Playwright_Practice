
from pathlib import Path

ROOT = Path(__file__).resolve().parent

IGNORE_DIRS = {
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".git",
    ".idea",
    "allure-results",
    "allure-report",
}

def print_structure(path: Path, prefix: str = ""):
    items = sorted(
        [
            item for item in path.iterdir()
            if item.name not in IGNORE_DIRS
            and not item.name.endswith(".pyc")
        ],
        key=lambda item: (item.is_file(), item.name.lower())
    )

    for index, item in enumerate(items):
        is_last = index == len(items) - 1

        connector = "└── " if is_last else "├── "
        print(prefix + connector + item.name)

        if item.is_dir():
            extension = "    " if is_last else "│   "
            print_structure(item, prefix + extension)


if __name__ == "__main__":
    print(ROOT.name)
    print_structure(ROOT)
