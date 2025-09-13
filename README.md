# === FILE: README.md ===
# Facebook Group Poster Bot - Windows (Python)


This is a minimal skeleton for the desktop app you requested. It contains:
- PySide6 UI skeleton
- SQLAlchemy models (SQLite)
- Playwright profile launcher
- Worker pool with `batch_size` concurrency manager
- Dry-run posting simulation (safe default) and placeholder for real post implementation


IMPORTANT: The `post_to_group()` function is intentionally left in "DRY RUN" mode by default. Do not change to real posting without understanding Facebook terms and risks.


## Quick start
1. Create a virtualenv and activate it.
2. pip install -r requirements.txt
3. python -m playwright install
4. Optional: edit `seed_sample.py` to add your Chrome profile paths or accounts.
5. python seed_sample.py # creates sample DB entries
6. python -m app.main # runs the minimal UI