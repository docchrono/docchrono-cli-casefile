"""Generate a deterministic fictional vendor due-diligence file set."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"


def rendered_files() -> dict[str, bytes]:
    return {
        "01_vendor_profile.txt": (
            b"On June 2, 2026, Ava Patel created Vendor #N-42 for Northstar Components.\n"
        ),
        "02_approval.eml": (
            b"From: Ian Brooks <ian.brooks@example.test>\n"
            b"To: Ava Patel <ava.patel@example.test>\n"
            b"Date: Thu, 4 Jun 2026 10:30:00 -0500\n"
            b"Subject: Vendor N-42 approval\n"
            b"Message-ID: <vendor-n42-approval@example.test>\n"
            b"MIME-Version: 1.0\n"
            b'Content-Type: text/plain; charset="utf-8"\n\n'
            b"On June 4, 2026, Ian Brooks approved Vendor #N-42.\n"
        ),
        "03_invoice_record.md": (
            b"# Invoice record\n\nOn June 9, 2026, Northstar Components paid Invoice #884.\n"
        ),
    }


def generate(destination: Path = DATA_DIR) -> tuple[Path, ...]:
    destination.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for filename, content in rendered_files().items():
        path = destination / filename
        path.write_bytes(content)
        paths.append(path)
    return tuple(paths)


def check(destination: Path = DATA_DIR) -> bool:
    expected = rendered_files()
    return (
        destination.exists()
        and {path.name for path in destination.iterdir() if path.is_file()} == set(expected)
        and all(
            (destination / filename).read_bytes() == content
            for filename, content in expected.items()
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        if not check():
            print("Synthetic data is missing or stale. Run: python generate_data.py")
            return 1
        print("Synthetic vendor records are deterministic and current.")
        return 0
    for path in generate():
        print(path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
