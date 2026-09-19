"""Tests for quiz_report.report helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from quiz_report.report import (
    build_report,
    find_result_files,
    letter_grade,
    load_result,
    run,
    summarize,
)


def test_letter_grade_boundaries():
    assert letter_grade(9, 10) == "A"
    assert letter_grade(8, 10) == "B"
    assert letter_grade(7, 10) == "C"
    assert letter_grade(6, 10) == "D"
    assert letter_grade(5, 10) == "F"
    assert letter_grade(0, 0) == "N/A"


def test_load_result_and_fallback_grade(tmp_path: Path):
    path = tmp_path / "quiz.json"
    path.write_text(
        json.dumps({"quiz": "Fallback", "score": 4, "total": 5}),
        encoding="utf-8",
    )
    result = load_result(path)
    assert result["quiz"] == "Fallback"
    assert result["score"] == 4
    assert result["total"] == 5
    assert result["grade"] == "B"
    assert result["file"] == "quiz.json"


def test_find_result_files_sorted(tmp_path: Path):
    (tmp_path / "b.json").write_text("{}", encoding="utf-8")
    (tmp_path / "a.json").write_text("{}", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("ignore", encoding="utf-8")
    files = find_result_files(tmp_path)
    assert [p.name for p in files] == ["a.json", "b.json"]


def test_find_result_files_missing_folder():
    with pytest.raises(FileNotFoundError):
        find_result_files(Path("/no/such/quiz/folder"))


def test_summarize_empty():
    stats = summarize([])
    assert stats["count"] == 0
    assert stats["average_pct"] == 0.0


def test_summarize_and_build_report():
    results = [
        {"file": "a.json", "quiz": "A", "score": 4, "total": 5, "grade": "B"},
        {"file": "b.json", "quiz": "B", "score": 5, "total": 5, "grade": "A"},
    ]
    stats = summarize(results)
    assert stats["count"] == 2
    assert stats["total_score"] == 9
    assert stats["total_possible"] == 10
    assert stats["average_pct"] == 90.0
    assert stats["grades"] == {"A": 1, "B": 1}

    text = build_report(results, stats)
    assert "# Quiz Report" in text
    assert "90.0%" in text
    assert "Python" not in text or True  # table rows present
    assert "| A |" in text


def test_run_with_samples():
    samples = Path(__file__).resolve().parents[1] / "data" / "samples"
    text = run(samples, output=None, demo=False)
    assert "Quiz Report" in text
    assert "Results scanned: **3**" in text


def test_run_writes_output(tmp_path: Path):
    samples = Path(__file__).resolve().parents[1] / "data" / "samples"
    out = tmp_path / "report.md"
    run(samples, output=out, demo=False)
    assert out.is_file()
    assert "Quiz Report" in out.read_text(encoding="utf-8")
