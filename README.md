# Job Project

## Running the backend

Run commands from the repository root (`Job-Project`). Activate your Python
virtual environment first:

macOS / Linux:

```sh
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the API with the same command on either platform:

```sh
python -m uvicorn app.main:app --app-dir backend --reload
```

`--app-dir backend` adds `backend` to Python's import search path, so imports
such as `from app.Model.user import User` resolve consistently. Keep backend
imports prefixed with `app.` and match directory capitalization exactly
(`Model`, `Controller`, `Service`, `Schema`). Avoid running `main.py` directly.

The backend requires MongoDB. Set `MONGODB_URI` in the process environment to
use another server; otherwise it connects to `mongodb://localhost:27017`.
