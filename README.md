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

The API starts at `http://127.0.0.1:8000`. All routes use the `/cafeteria` root prefix. Check it with `GET /cafeteria/health`.

Access tokens last `JWT_EXPIRES_MINUTES` minutes. Admin refresh tokens last `JWT_REFRESH_EXPIRES_DAYS` days; the defaults are 60 minutes and 7 days.

## Portal-oriented structure

Portal-owned code is grouped by URL prefix in every layered module. This lets a developer follow an admin request through `routes/admin.py`, `controllers/admin`, `validations/admin`, and `services/admin` without mixing it with student or shop code.

```text
routes/
|-- admin.py
|-- api.py
`-- shop.py
controllers/
|-- admin/
|-- api/
|-- shop/
`-- shared/
validations/
|-- admin/
|-- api/
|-- shop/
`-- shared/
services/
|-- admin/
|-- api/
|-- shop/
`-- shared/
```

The `shop` packages are ready for future shop-portal features. Code used by more than one portal, such as pagination, token handling, and common field validation, belongs in `shared`. Models, helpers, middleware, and database files stay shared because they describe the whole application rather than a single portal.

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
GET /cafeteria/admin/users?page=1&per_page=20
```

Collection responses contain both `data` and `pagination`. Option endpoints are the exception and return a normal, non-paginated list of active records.

## List filters

Filters are combined with pagination, for example:

```text
GET /cafeteria/admin/users?page=1&per_page=20&search=alice&role_id=3&is_active=true
```

Supported filters are:

| Collection | Filter parameters |
| --- | --- |
| Admin roles | `search`, `is_active` |
| Admin users | `search`, `is_active`, `role_id`, `department_id`, `type` |
| Admin categories | `search`, `is_active` |
| Admin genres | `search`, `is_active` |
| Admin payment methods | `search`, `is_active`, `type` |
| Admin shops | `search`, `is_active` |
| Admin shop staff | `search`, `is_active` |
| Admin shop payment accounts | `search`, `is_active`, `payment_method_id` |
| Public shops | `search` |
| Public shop menus | `search`, `genre_id`, `min_cost`, `max_cost` |

Boolean filters accept `true`, `false`, `1`, or `0`. Unknown filters and invalid values return a `422` response with field-level errors. Public shop and menu lists continue to return active and available records only.

### Roles list parameters

`GET /cafeteria/admin/roles` accepts:

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `page` | positive integer | No | Page number; default is `1` |
| `per_page` | positive integer | No | Items per page; default is `20`, maximum is `100` |
| `search` | string | No | Partial, case-insensitive search against the role name |
| `is_active` | boolean | No | Filter active or inactive roles; accepts `true`, `false`, `1`, or `0` |

Examples:

```text
GET /cafeteria/admin/roles?page=1&per_page=20
GET /cafeteria/admin/roles?search=admin
GET /cafeteria/admin/roles?is_active=true
GET /cafeteria/admin/roles?search=staff&is_active=true&page=1&per_page=10
```

## Local file storage

Uploads currently use project-local storage configured in `.env`:

```env
STORAGE=local
LOCAL_STORAGE_PATH=uploads
MAX_UPLOAD_MB=5
ALLOWED_UPLOAD_EXTENSIONS=["jpg","jpeg","png","webp","gif","pdf"]
```

All upload behavior is kept in `helpers/file_uploader.py`; uploads do not use controller, service, or validation modules. Upload a file as admin with a `multipart/form-data` request whose field name is `file`:

```text
POST /cafeteria/admin/uploads
```

The response returns a URL such as `/cafeteria/uploads/abc123.png`. Local files are available through `GET /cafeteria/uploads/{filename}`. Uploaded content is ignored by Git; only the empty `uploads/` folder is retained. Additional drivers such as S3 can be added later through the same file-uploader helper.

## Endpoints

- `GET /cafeteria/health`
- `POST /cafeteria/api/auth/login` for students with `{ "email": "student@example.com", "password": "..." }`. Student login accepts an email address only.
- `POST /cafeteria/api/auth/logout` for students with a bearer token
- `POST /cafeteria/admin/auth/login` for administrators with `{ "email": "admin@example.com", "password": "..." }`. Admin login accepts an email address only.
- `POST /cafeteria/admin/auth/refresh-token` accepts `{ "refresh_token": "..." }` without an access token and returns a rotated access/refresh token pair.
- `POST /cafeteria/admin/auth/logout` for administrators with a bearer token
- `GET /cafeteria/admin/auth/profile` returns the authenticated administrator profile
- `POST /cafeteria/admin/auth/revoke-token` revokes its admin Bearer token. Correctly signed expired tokens are accepted on this endpoint, and no JSON body is required.
- `GET /cafeteria/api/shops`
- `GET /cafeteria/api/shops/{shop_id}/menus`

All endpoints below require an admin bearer token:

- Roles: `GET|POST /cafeteria/admin/roles`, `GET|PUT|DELETE /cafeteria/admin/roles/{role_id}`
- Role options: `GET /cafeteria/admin/role-options`
- Users: `GET|POST /cafeteria/admin/users`, `GET|PUT|DELETE /cafeteria/admin/users/{user_id}`
- Categories: `GET|POST /cafeteria/admin/categories`, `GET|PUT|DELETE /cafeteria/admin/categories/{category_id}`
- Category options: `GET /cafeteria/admin/category-options`
- Genres: `GET|POST /cafeteria/admin/genres`, `GET|PUT|DELETE /cafeteria/admin/genres/{genre_id}`
- Genre options: `GET /cafeteria/admin/genre-options`
- Payment methods: `GET|POST /cafeteria/admin/payment-methods`, `GET|PUT|DELETE /cafeteria/admin/payment-methods/{method_id}`
- Payment method options: `GET /cafeteria/admin/payment-method-options`
- Shops: `GET|POST /cafeteria/admin/shops`, `GET|PUT|DELETE /cafeteria/admin/shops/{shop_id}`
- Shop staff: `GET|POST /cafeteria/admin/shops/{shop_id}/staffs`, `GET|PUT|DELETE /cafeteria/admin/shops/{shop_id}/staffs/{staff_id}`
- Shop payment accounts: `GET|POST /cafeteria/admin/shops/{shop_id}/payment-accounts`, `GET|PUT|DELETE /cafeteria/admin/shops/{shop_id}/payment-accounts/{account_id}`
- File upload: `POST /cafeteria/admin/uploads` using `multipart/form-data`

Portal prefixes are organized as:

```text
/cafeteria/admin  Admin portal
/cafeteria/api    Student/public API
/cafeteria/shop   Shop portal (ready for future shop endpoints)
```

Run `python manage.py test` for the test suite and `python manage.py migrate --sql` to validate offline migration generation.
