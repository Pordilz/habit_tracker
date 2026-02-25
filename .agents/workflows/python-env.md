---
description: Python environment conventions for the habit_tracker project
---

# Python Environment Rules

## Interpreter
- **Always** use the virtual environment Python at `.venv/bin/python` (absolute: `/Users/yahyaparuk/University/IU/Python Project/PHASE 2/habit_tracker/.venv/bin/python`)
- The venv was created with Python 3.14 from `/opt/homebrew/bin/python3`

## Running Commands
// turbo-all
1. Run the app: `.venv/bin/python main.py`
2. Run tests: `.venv/bin/python -m pytest`
3. Install packages: `.venv/bin/pip install <package>`

## Important
- Never use the system Python directly; always use `.venv/bin/python`
- If the venv is missing, recreate it: `/opt/homebrew/bin/python3 -m venv .venv`
