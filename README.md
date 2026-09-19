# quiz-report

Folder of scores in. Markdown out. No dashboard. No cloud. No feelings.

`pathlib` walks a folder of quiz JSON. It tallies. It writes a report you can
open in a text editor. Someone has to grade the robots.

Python 3.10+. Tests exist. Slide decks do not.

## Install

```bash
git clone https://github.com/Trench-Worker/quiz-report.git
cd quiz-report

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

Or skip the ritual:

```bash
PYTHONPATH=src python -m quiz_report --input data/samples --demo
```

## Run

```bash
python -m quiz_report --input data/samples --demo
```

That's the one. Bundled samples. Three quizzes. One of them is a D. The file did
that to itself.

Want a file instead of a terminal dump:

```bash
python -m quiz_report --input data/samples --output report.md
```

After install, `quiz-report` also works.

| Flag | What it does |
|------|----------------|
| `--input PATH` | Folder of `*.json`. Required. Non-recursive. Everything else is ignored. |
| `--output PATH` | Write the markdown here. |
| `--demo` | Print to stdout. Also the default if you omit `--output`. |

## Input

Each file is one object. `score` and `total` are required. `quiz` and `grade`
are optional. Missing grade? It invents one. That's the job.

```json
{"quiz": "Python Basics", "score": 4, "total": 5, "grade": "B"}
```

Drop more `*.json` in `--input` and re-run. `.txt` files can sit there and think
about what they've done.

## Tests

```bash
pytest
```

Covers the boring parts that matter: `letter_grade`, `load_result`,
`find_result_files`, `summarize`, write-to-disk.

## CI

GitHub Actions. Ubuntu. Python 3.12. Installs `.[dev]`, runs `pytest`, then:

```bash
python -m quiz_report --input data/samples --demo
```

So the CLI still works when nobody is there to open the report.

## License

MIT. See [LICENSE](LICENSE).
