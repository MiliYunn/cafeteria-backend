# Graph Report - apcafeteria-backend  (2026-08-27)

## Corpus Check
- 147 files · ~13,796 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 630 nodes · 1649 edges · 71 communities (54 shown, 17 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 142 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0d4323b1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- admin.py
- extensions.py
- fields.py
- ValidationError
- app.py
- get_record
- PaymentAccountService
- jwt.py
- schema.sql
- paginated_response
- test_helpers.py
- ShopStaffService
- Role
- APCafeteria Backend
- jwt_auth.py
- manage.py
- controllers/admin/__init__.py
- controllers/api/__init__.py
- controllers/shared/__init__.py
- controllers/shop/__init__.py
- database/__init__.py
- seeders/__init__.py
- helpers/__init__.py
- middlewares/__init__.py
- services/admin/__init__.py
- services/api/__init__.py
- services/shared/__init__.py
- services/shop/__init__.py
- validations/admin/__init__.py
- validations/api/__init__.py
- validations/__init__.py
- validations/shared/__init__.py
- validations/shop/__init__.py
- APCafeteria Backend
- shared/auth_service.py
- api.py

## God Nodes (most connected - your core abstractions)
1. `success_response()` - 59 edges
2. `ValidationError` - 50 edges
3. `get_record()` - 34 edges
4. `SerializableMixin` - 32 edges
5. `commit_record()` - 26 edges
6. `apply_collection_filters()` - 25 edges
7. `validate_resource_payload()` - 25 edges
8. `paginated_response()` - 23 edges
9. `pagination_parameters()` - 21 edges
10. `paginate_records()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `register_error_handlers()` --uses--> `ValidationError`  [INFERRED]
  app.py → validations/shared/exceptions.py
- `list_shop_staffs()` --uses--> `ShopStaffService`  [INFERRED]
  controllers/admin/shop_staff_controller.py → services/admin/shop_staff_service.py
- `_jwt_required()` --uses--> `TokenService`  [INFERRED]
  middlewares/jwt_auth.py → services/shared/token_service.py
- `CategoryService` --uses--> `Category`  [INFERRED]
  services/admin/category_service.py → models/category.py
- `GenreService` --uses--> `Genre`  [INFERRED]
  services/admin/genre_service.py → models/genre.py

## Import Cycles
- None detected.

## Communities (71 total, 17 thin omitted)

### Community 0 - "admin.py"
Cohesion: 0.07
Nodes (43): admin_login(), admin_logout(), admin_profile(), admin_refresh_token(), admin_revoke_token(), create_genre(), delete_genre(), genre_options() (+35 more)

### Community 1 - "extensions.py"
Cohesion: 0.13
Nodes (22): Decimal, DeclarativeBase, Base, Shared Flask extension instances., Any, Common model serialization helpers., SerializableMixin, Category (+14 more)

### Community 2 - "fields.py"
Cohesion: 0.16
Nodes (26): Admin authentication payload validation., Category payload validation., _optional_email(), Any, validate_shop_staff(), Any, Student API authentication payload validation., validate_api_login() (+18 more)

### Community 3 - "ValidationError"
Cohesion: 0.13
Nodes (33): Exception, FilterRule, test_admin_filters_convert_query_values(), test_menu_price_filters_are_validated(), test_unknown_and_invalid_filters_return_field_errors(), Any, Validated filter parameters for admin collection endpoints., Roles support: search (name) and is_active (boolean). (+25 more)

### Community 5 - "app.py"
Cohesion: 0.06
Nodes (38): create_app(), Flask, Flask application factory., register_error_handlers(), FlaskConfig, _json_list(), Environment-backed application configuration., Settings (+30 more)

### Community 6 - "get_record"
Cohesion: 0.09
Nodes (31): ColumnElement, category_options(), create_category(), delete_category(), get_category(), list_categories(), update_category(), create_shop() (+23 more)

### Community 7 - "PaymentAccountService"
Cohesion: 0.25
Nodes (8): create_payment_account(), delete_payment_account(), get_payment_account(), list_payment_accounts(), update_payment_account(), PaymentAccountService, Any, validate_payment_account()

### Community 8 - "jwt.py"
Cohesion: 0.35
Nodes (10): create_refresh_token(), decode_access_token(), decode_refresh_token(), _decode_token(), Any, JWT encoding and decoding., ActiveAdmin, test_admin_refresh_rejects_revoked_refresh_token() (+2 more)

### Community 9 - "schema.sql"
Cohesion: 0.27
Nodes (15): categories, genres, menus, order_logs, order_menus, orders, payment_accounts, payment_methods (+7 more)

### Community 10 - "paginated_response"
Cohesion: 0.10
Nodes (24): list_shop_staffs(), create_user(), delete_user(), get_user(), list_users(), update_user(), list_shop_menus(), list_shops() (+16 more)

### Community 11 - "test_helpers.py"
Cohesion: 0.29
Nodes (9): hash_password(), Password hashing helpers., verify_password(), create_access_token(), test_admin_revoke_accepts_its_expired_bearer_token(), test_access_token_round_trip(), test_invalid_login_payload_has_field_errors(), test_password_hash_round_trip() (+1 more)

### Community 12 - "ShopStaffService"
Cohesion: 0.30
Nodes (5): create_shop_staff(), delete_shop_staff(), get_shop_staff(), update_shop_staff(), ShopStaffService

### Community 13 - "Role"
Cohesion: 0.40
Nodes (7): seed_admin_user(), seed_payment_methods(), seed_roles(), Run all idempotent seeders in dependency order., run_seeders(), Role, User

### Community 14 - "APCafeteria Backend"
Cohesion: 0.20
Nodes (9): APCafeteria Backend, Endpoints, List filters, Local file storage, Pagination, Portal-oriented structure, Project commands, Roles list parameters (+1 more)

### Community 15 - "jwt_auth.py"
Cohesion: 0.40
Nodes (5): _jwt_required(), jwt_revoke_required(), JWT authentication and role authorization decorators., Require a valid, unexpired access token., Require a signed access token while allowing it to be expired.

### Community 16 - "manage.py"
Cohesion: 0.27
Nodes (9): ArgumentParser, build_parser(), dispatch(), main(), Unified command runner for APCafeteria backend development tasks., Run a project command with the current Python interpreter., run_command(), Namespace (+1 more)

### Community 65 - "APCafeteria Backend"
Cohesion: 0.40
Nodes (4): APCafeteria Backend, Architecture invariants, Database synchronization, Security and verification

### Community 69 - "shared/auth_service.py"
Cohesion: 0.29
Nodes (7): datetime, AuthService, _create_token_pair(), Authentication and refresh-token workflows., datetime, JWT revocation workflows., TokenService

### Community 70 - "api.py"
Cohesion: 0.22
Nodes (7): student_login(), student_logout(), api_rate_limit(), Central rate-limit extension and named policies., Public API endpoint registration only., ApiAuthService, datetime

## Knowledge Gaps
- **10 isolated node(s):** `Setup`, `Portal-oriented structure`, `Project commands`, `Pagination`, `Roles list parameters` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ValidationError` connect `ValidationError` to `admin.py`, `extensions.py`, `fields.py`, `shared/auth_service.py`, `app.py`, `PaymentAccountService`, `get_record`, `api.py`, `paginated_response`, `jwt.py`, `ShopStaffService`, `test_helpers.py`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Why does `success_response()` connect `admin.py` to `app.py`, `api.py`, `get_record`, `PaymentAccountService`, `paginated_response`, `ShopStaffService`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `get_record()` connect `get_record` to `admin.py`, `extensions.py`, `ValidationError`, `PaymentAccountService`, `paginated_response`, `ShopStaffService`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `ValidationError` (e.g. with `register_error_handlers()` and `AdminAuthService`) actually correct?**
  _`ValidationError` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Setup`, `Portal-oriented structure`, `Project commands` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `admin.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0733099209833187 - nodes in this community are weakly interconnected._
- **Should `extensions.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1321353065539112 - nodes in this community are weakly interconnected._