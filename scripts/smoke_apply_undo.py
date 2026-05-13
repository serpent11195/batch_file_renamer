from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT_DIR = Path(__file__).resolve().parents[1]

def run_command(command, cwd):
    result = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print("Command failed:")
        print(command)
        print("\nSTDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        sys.exit(result.returncode)

    return result

def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        test_dir = temp_path / "files"
        test_dir.mkdir()

        original_files = [
            "A Test File.txt",
            "Another File.txt",
        ]

        for file_name in original_files:
            (test_dir / file_name).write_text("sample", encoding="utf-8")

        run_command(
            f'python src/main.py apply --path "{test_dir}" --mode normalize',
            cwd=ROOT_DIR,
        )

        normalized_files = [p.name for p in test_dir.iterdir() if p.is_file()]
        print("After apply:", normalized_files)

        run_command(
            "python src/main.py undo",
            cwd=ROOT_DIR,
        )

        restored_files = sorted(p.name for p in test_dir.iterdir() if p.is_file())
        expected_files = sorted(original_files)

        if restored_files != expected_files:
            print("Undo did not restore original filenames.")
            print("Expected:", expected_files)
            print("Actual:", restored_files)
            sys.exit(1)

        print("Smoke apply/undo: OK")

if __name__ == "__main__":
    main()