"""Backend unit tests; run with python -m unittest discover -s backend -v."""

import sys
from pathlib import Path


# Match uvicorn's --app-dir backend import path when running from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
