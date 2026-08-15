from __future__ import annotations

from pathlib import Path

import demo
import pytest
from generate_data import check, generate

from docchrono import Case


def test_cli_build_inspect_and_timeline(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    data_dir = checkout / "data"
    case_path = checkout / "output" / "vendor.case.json"
    generate(data_dir)
    assert check(data_dir)
    case_path.parent.mkdir()

    completed = demo.run_cli(
        ["build", "data", "--strict", "--output", "output/vendor.case.json", "--json"],
        cwd=checkout,
    )
    assert completed.returncode == 0, completed.stderr
    assert '"complete": true' in completed.stdout

    completed = demo.run_cli(["inspect", "output/vendor.case.json", "--json"], cwd=checkout)
    assert completed.returncode == 0, completed.stderr
    assert '"documents": 3' in completed.stdout

    completed = demo.run_cli(["timeline", "output/vendor.case.json"], cwd=checkout)
    assert completed.returncode == 0, completed.stderr
    timeline_output = completed.stdout
    assert "Sources:" in timeline_output
    assert any(name in timeline_output for name in ("01_vendor_profile.txt", "02_approval.eml"))

    case = Case.load(case_path)
    assert case.report.complete
    assert len(case.documents) == 3
    assert case.events
    assert case.relationships


def test_documented_demo_runs_from_repository_root(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data_dir = tmp_path / "data"
    case = demo.run_demo(data_dir, tmp_path / "vendor.case.json")

    assert case.report.complete
    output = capsys.readouterr().out
    assert "$ docchrono build" in output
    assert "$ docchrono inspect" in output
    assert "$ docchrono timeline" in output
    expected = (demo.ROOT / "expected_output.txt").read_text(encoding="utf-8")
    assert output == expected
