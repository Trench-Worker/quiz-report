# quiz-report

Your quiz JSON files are sitting in a folder. This CLI walks that folder with
`pathlib`, tallies the scores, and writes a markdown report. No dashboards.
No cloud. Just files.

Built by **Trench-Worker** — because someone has to grade the robots.

## Why this exists

- Practice `Path.glob` / `iterdir` without inventing a startup
- Packaging + venv habits that survive contact with real projects
- A report you can actually open in a text editor

## Quick start

```bash
cd quiz-report
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Demo against the bundled samples
python -m quiz_report --input data/samples --demo

# Or write a file
python -m quiz_report --input data/samples --output report.md
```

## Sample input

Each JSON file looks like:

```json
{"quiz": "Python Basics", "score": 4, "total": 5, "grade": "B"}
```

Drop more files in `--input` and re-run. The scanner only cares about `*.json`.

## Tests

```bash
pytest
```

## License

MIT © 2026 Trench-Worker
