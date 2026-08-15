"""Exercise DocChrono's build, inspect, and timeline CLI commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from generate_data import DATA_DIR, generate

from docchrono import Case

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
CASE_PATH = OUTPUT_DIR / "vendor.case.json"


def console_script_path() -> Path:
    """Locate the installed DocChrono entry point beside this Python executable."""

    script_name = "docchrono.exe" if sys.platform == "win32" else "docchrono"
    script = Path(sys.executable).with_name(script_name)
    if not script.is_file():
        raise RuntimeError(
            f"DocChrono console script not found beside {sys.executable}; "
            "install requirements.txt into this environment"
        )
    return script


def run_cli(arguments: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    """Run the installed console script and capture its complete result."""

    return subprocess.run(
        [str(console_script_path()), *arguments],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def stable_output(output: str, case_path: Path) -> str:
    """Replace the machine-specific saved path with the documented relative path."""

    return output.replace(str(case_path.resolve()), "output/vendor.case.json")


def run_demo(data_dir: Path = DATA_DIR, case_path: Path = CASE_PATH) -> Case:
    if not data_dir.exists():
        generate(data_dir)
    case_path.parent.mkdir(parents=True, exist_ok=True)

    commands = (
        (
            "docchrono build data --strict --output output/vendor.case.json",
            ["build", str(data_dir), "--strict", "--output", str(case_path)],
        ),
        (
            "docchrono inspect output/vendor.case.json --json",
            ["inspect", str(case_path), "--json"],
        ),
        (
            "docchrono timeline output/vendor.case.json",
            ["timeline", str(case_path)],
        ),
    )
    for index, (display, arguments) in enumerate(commands):
        print(f"$ {display}")
        completed = run_cli(arguments)
        print(stable_output(completed.stdout, case_path).rstrip("\n"))
        print(completed.stderr, end="", file=sys.stderr)
        if completed.returncode != 0:
            raise RuntimeError(f"Command failed with status {completed.returncode}: {display}")
        if index + 1 < len(commands):
            print()
    return Case.load(case_path)


if __name__ == "__main__":
    run_demo()
