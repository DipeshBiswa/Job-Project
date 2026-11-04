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

## Running backend tests

With your virtual environment activated, install dependencies and run the suite
from the repository root:

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s backend -v
```

Tests live in `backend/tests` and use Python's built-in `unittest` framework.
They cover the user model, user and authentication services, JWT creation, and
the user controller's HTTP endpoints, including validation and error responses.
Database operations are mocked; no MongoDB server or configured JWT secret is
needed. Controller tests mount the production router in a test application so
the database startup hook does not run.

To run just one test file:

```sh
python -m unittest discover -s backend -p 'test_user_service.py' -v
```

The root-level `test_connection.py` is a separate manual MongoDB connectivity
check and is excluded by the backend test command above.
