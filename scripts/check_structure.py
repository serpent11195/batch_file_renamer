from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    ".gitignore",
    "src",
    "src/main.py",
    "tests",
]

OPTIONAL_PATHS = [
    "requirements-dev.txt",
    "pytest.ini",
    "mini-ci.yml",
    "sample_files",
    "data",
]

def check_paths(paths):
    missing = []

    for path in paths:
        full_path = ROOT_DIR / path
        if not full_path.exists():
            missing.append(path)

    return missing

def main():
    missing_required = check_paths(REQUIRED_PATHS)
    missing_optional = check_paths(OPTIONAL_PATHS)

    if missing_required:
        print("Missing required project paths:")
        for path in missing_required:
            print(f"- {path}")
        sys.exit(1)

    print("Required project structure: OK")

    if missing_optional:
        print("\nOptional paths not found:")
        for path in missing_optional:
            print(f"- {path}")
    else:
        print("Optional project structure: OK")

    sys.exit(0)

if __name__ == "__main__":
    main()