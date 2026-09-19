"""Scan a folder of quiz-result JSON files and write a markdown summary.

Uses pathlib for discovery and writing — no os.path gymnastics required.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def letter_grade(score: int, total: int) -> str:
    """Map a score/total ratio to a simple letter grade."""
    if total <= 0:
        return "N/A"
    pct = (score / total) * 100
    if pct >= 90:
        return "A"
    if pct >= 80:
        return "B"
    if pct >= 70:
        return "C"
    if pct >= 60:
        return "D"
    return "F"


def load_result(path: Path) -> dict:
    """Parse one quiz-result JSON file into a normalized dict."""
    data = json.loads(path.read_text(encoding="utf-8"))
    score = int(data["score"])
    total = int(data["total"])
    grade = data.get("grade") or letter_grade(score, total)
    return {
        "file": path.name,
        "quiz": str(data.get("quiz", path.stem)),
        "score": score,
        "total": total,
        "grade": str(grade),
    }


def find_result_files(folder: Path) -> list[Path]:
    """Return sorted *.json paths under folder (non-recursive)."""
    if not folder.is_dir():
        raise FileNotFoundError(f"Input folder not found: {folder}")
    return sorted(folder.glob("*.json"))


def summarize(results: list[dict]) -> dict:
    """Compute aggregate stats from parsed results."""
    count = len(results)
    if count == 0:
        return {
            "count": 0,
            "total_score": 0,
            "total_possible": 0,
            "average_pct": 0.0,
            "grades": {},
        }

    total_score = sum(r["score"] for r in results)
    total_possible = sum(r["total"] for r in results)
    average_pct = (total_score / total_possible) * 100 if total_possible else 0.0

    grades: dict[str, int] = {}
    for r in results:
        grades[r["grade"]] = grades.get(r["grade"], 0) + 1

    return {
        "count": count,
        "total_score": total_score,
        "total_possible": total_possible,
        "average_pct": round(average_pct, 1),
        "grades": grades,
    }


def build_report(results: list[dict], stats: dict) -> str:
    """Render a short markdown report from results + summary stats."""
    lines = [
        "# Quiz Report",
        "",
        f"- Results scanned: **{stats['count']}**",
        f"- Points: **{stats['total_score']}** / **{stats['total_possible']}**",
        f"- Average: **{stats['average_pct']}%**",
        "",
    ]

    if stats["grades"]:
        grade_bits = ", ".join(f"{g}: {n}" for g, n in sorted(stats["grades"].items()))
        lines.append(f"- Grades: {grade_bits}")
        lines.append("")

    lines.extend(["## Details", ""])
    if not results:
        lines.append("_No quiz result files found._")
        lines.append("")
    else:
        lines.append("| Quiz | Score | Grade | File |")
        lines.append("| --- | --- | --- | --- |")
        for r in results:
            lines.append(
                f"| {r['quiz']} | {r['score']}/{r['total']} | {r['grade']} | `{r['file']}` |"
            )
        lines.append("")

    return "\n".join(lines)


def run(input_dir: Path, output: Path | None = None, demo: bool = False) -> str:
    """Scan input_dir, build report text, optionally write it, return the text."""
    files = find_result_files(input_dir)
    results = [load_result(p) for p in files]
    stats = summarize(results)
    text = build_report(results, stats)

    if output is not None:
        output.write_text(text, encoding="utf-8")
    if demo or output is None:
        print(text)

    return text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quiz-report",
        description="Scan quiz result JSON files and write a markdown summary.",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Folder of quiz result *.json files",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Write report markdown to this path",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Print the report to stdout (also default when --output is omitted)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        run(input_dir=args.input, output=args.output, demo=args.demo)
    except FileNotFoundError as exc:
        print(f"error: {exc}")
        return 1
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: bad quiz result file — {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
