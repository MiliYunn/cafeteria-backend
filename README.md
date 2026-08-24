# APCafeteria Backend

Flask 3 / Python 3.13 API for APCafeteria, backed by MySQL and Alembic.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env  # only if .env does not already exist
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

## Pagination

Every collection endpoint accepts `page` and `per_page`. The default is 20 records per page and the maximum is 100:

```text
GET /api/admin/users?page=1&per_page=20
```

Collection responses contain both `data` and `pagination`. Option endpoints are the exception and return a normal, non-paginated list of active records.

## Endpoints

- `GET /health`
- `POST /api/auth/login` for students with `{ "login": "...", "password": "..." }`
- `POST /api/auth/logout` for students with a bearer token
- `POST /api/admin/auth/login` for administrators with `{ "login": "...", "password": "..." }`
- `POST /api/admin/auth/logout` for administrators with a bearer token
- `GET /api/shops`
- `GET /api/shops/{shop_id}/menus`

All endpoints below require an admin bearer token:

- Roles: `GET|POST /api/admin/roles`, `GET|PUT|DELETE /api/admin/roles/{role_id}`
- Role options: `GET /api/admin/role-options`
- Users: `GET|POST /api/admin/users`, `GET|PUT|DELETE /api/admin/users/{user_id}`
- Categories: `GET|POST /api/admin/categories`, `GET|PUT|DELETE /api/admin/categories/{category_id}`
- Category options: `GET /api/admin/category-options`
- Genres: `GET|POST /api/admin/genres`, `GET|PUT|DELETE /api/admin/genres/{genre_id}`
- Genre options: `GET /api/admin/genre-options`
- Payment methods: `GET|POST /api/admin/payment-methods`, `GET|PUT|DELETE /api/admin/payment-methods/{method_id}`
- Payment method options: `GET /api/admin/payment-method-options`
- Shops: `GET|POST /api/admin/shops`, `GET|PUT|DELETE /api/admin/shops/{shop_id}`
- Shop staff: `GET|POST /api/admin/shops/{shop_id}/staffs`, `GET|PUT|DELETE /api/admin/shops/{shop_id}/staffs/{staff_id}`
- Shop payment accounts: `GET|POST /api/admin/shops/{shop_id}/payment-accounts`, `GET|PUT|DELETE /api/admin/shops/{shop_id}/payment-accounts/{account_id}`

Run `python manage.py test` for the test suite and `python manage.py migrate --sql` to validate offline migration generation.
