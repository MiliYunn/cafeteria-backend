# APCafeteria Backend

Flask 3 / Python 3.13 API for APCafeteria, backed by MySQL and Alembic.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env  # only if .env does not already exist
alembic upgrade head
python -m database.seeders.run
python run.py
```

The API starts at `http://127.0.0.1:8000`. Check it with `GET /health`.

## Project commands

Use `manage.py` as the single entry point for common commands:

```powershell
python manage.py migrate                 # alembic upgrade head
python manage.py migrate --sql           # preview upgrade SQL
python manage.py downgrade               # alembic downgrade -1
python manage.py revision "add table"     # create an empty revision
python manage.py revision "add table" --autogenerate
python manage.py current
python manage.py history
python manage.py heads
python manage.py stamp head
python manage.py seed
python manage.py test
python manage.py run
```

Run `python manage.py --help` or `python manage.py <command> --help` for command details.

## Initial endpoints

- `GET /health`
- `POST /api/auth/login` for students with `{ "login": "...", "password": "..." }`
- `POST /api/auth/logout` for students with a bearer token
- `POST /api/admin/auth/login` for administrators with `{ "login": "...", "password": "..." }`
- `POST /api/admin/auth/logout` for administrators with a bearer token
- `GET /api/shops`
- `GET /api/shops/{shop_id}/menus`
- `GET /api/admin/users` (admin JWT)
- `GET|POST /api/admin/categories` (admin JWT)

Run `python manage.py test` for the test suite and `python manage.py migrate --sql` to validate offline migration generation.
