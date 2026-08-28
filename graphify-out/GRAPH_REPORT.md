# Graph Report - apcafeteria-backend  (2026-08-29)

## Corpus Check
- 149 files · ~14,558 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 646 nodes · 1694 edges · 68 communities (51 shown, 17 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 150 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b1935245`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- admin.py
- extensions.py
- fields.py
- admin/filters.py
- app.py
- get_record
- PaymentAccountService
- schema.sql
- user_controller.py
- shop_staff_controller.py
- APCafeteria Backend
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
- ValidationError
- api.py

## God Nodes (most connected - your core abstractions)
1. `success_response()` - 59 edges
2. `ValidationError` - 52 edges
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
- `list_payment_accounts()` --uses--> `PaymentAccountService`  [INFERRED]
  controllers/admin/payment_account_controller.py → services/admin/payment_account_service.py
- `list_shops()` --uses--> `ShopService`  [INFERRED]
  controllers/admin/shop_controller.py → services/admin/shop_service.py
- `list_shop_staffs()` --uses--> `ShopStaffService`  [INFERRED]
  controllers/admin/shop_staff_controller.py → services/admin/shop_staff_service.py
- `list_users()` --uses--> `UserService`  [INFERRED]
  controllers/admin/user_controller.py → services/admin/user_service.py

## Import Cycles
- None detected.

## Communities (68 total, 17 thin omitted)

### Community 0 - "admin.py"
Cohesion: 0.07
Nodes (51): category_options(), create_category(), delete_category(), get_category(), list_categories(), update_category(), create_genre(), delete_genre() (+43 more)

### Community 1 - "extensions.py"
Cohesion: 0.13
Nodes (22): seed_payment_methods(), seed_roles(), Run all idempotent seeders in dependency order., run_seeders(), Decimal, DeclarativeBase, Base, Shared Flask extension instances. (+14 more)

### Community 2 - "fields.py"
Cohesion: 0.12
Nodes (30): test_paginated_response_shape(), test_pagination_defaults_and_limit(), test_role_create_and_update_validation(), test_user_password_is_required_only_when_creating(), Any, Admin authentication payload validation., validate_admin_login(), validate_refresh_token() (+22 more)

### Community 3 - "admin/filters.py"
Cohesion: 0.13
Nodes (33): FilterRule, test_admin_filters_convert_query_values(), test_collection_filters_use_bound_sql_parameters(), test_menu_price_filters_are_validated(), test_unknown_and_invalid_filters_return_field_errors(), Any, Validated filter parameters for admin collection endpoints., Roles support: search (name) and is_active (boolean). (+25 more)

### Community 5 - "app.py"
Cohesion: 0.06
Nodes (39): create_app(), Flask, Flask application factory., register_error_handlers(), FlaskConfig, _json_list(), Environment-backed application configuration., Settings (+31 more)

### Community 6 - "get_record"
Cohesion: 0.11
Nodes (29): ColumnElement, create_shop(), delete_shop(), get_shop(), update_shop(), Shop, parametrize, Select (+21 more)

### Community 7 - "PaymentAccountService"
Cohesion: 0.26
Nodes (8): create_payment_account(), delete_payment_account(), get_payment_account(), update_payment_account(), PaymentAccount, PaymentAccountService, Any, validate_payment_account()

### Community 9 - "schema.sql"
Cohesion: 0.27
Nodes (15): categories, genres, menus, order_logs, order_menus, orders, payment_accounts, payment_methods (+7 more)

### Community 10 - "user_controller.py"
Cohesion: 0.28
Nodes (8): create_user(), delete_user(), get_user(), update_user(), _serialize(), UserService, Any, validate_user()

### Community 12 - "shop_staff_controller.py"
Cohesion: 0.27
Nodes (8): create_shop_staff(), delete_shop_staff(), get_shop_staff(), update_shop_staff(), ShopStaff, ShopStaffService, Any, validate_shop_staff()

### Community 14 - "APCafeteria Backend"
Cohesion: 0.18
Nodes (10): APCafeteria Backend, Endpoints, List filters, Local file storage, Pagination, Portal-oriented structure, Project commands, Roles list parameters (+2 more)

### Community 16 - "manage.py"
Cohesion: 0.27
Nodes (9): ArgumentParser, build_parser(), dispatch(), main(), Unified command runner for APCafeteria backend development tasks., Run a project command with the current Python interpreter., run_command(), Namespace (+1 more)

### Community 65 - "APCafeteria Backend"
Cohesion: 0.40
Nodes (4): APCafeteria Backend, Architecture invariants, Database synchronization, Security and verification

### Community 69 - "ValidationError"
Cohesion: 0.07
Nodes (48): admin_login(), admin_logout(), admin_profile(), admin_refresh_token(), admin_revoke_token(), seed_admin_user(), Exception, hash_password() (+40 more)

### Community 70 - "api.py"
Cohesion: 0.20
Nodes (9): student_login(), student_logout(), api_rate_limit(), Central rate-limit extension and named policies., Public API endpoint registration only., datetime, Any, Student API authentication payload validation. (+1 more)

## Knowledge Gaps
- **11 isolated node(s):** `Setup`, `Shop opening and closing hours`, `Portal-oriented structure`, `Project commands`, `Pagination` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ValidationError` connect `ValidationError` to `admin.py`, `fields.py`, `admin/filters.py`, `app.py`, `get_record`, `PaymentAccountService`, `user_controller.py`, `shop_staff_controller.py`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `success_response()` connect `admin.py` to `ValidationError`, `get_record`, `PaymentAccountService`, `api.py`, `app.py`, `user_controller.py`, `shop_staff_controller.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `get_record()` connect `get_record` to `admin.py`, `ValidationError`, `PaymentAccountService`, `user_controller.py`, `shop_staff_controller.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ValidationError` (e.g. with `register_error_handlers()` and `AdminAuthService`) actually correct?**
  _`ValidationError` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Setup`, `Shop opening and closing hours`, `Portal-oriented structure` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `admin.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06835443037974684 - nodes in this community are weakly interconnected._
- **Should `extensions.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12682926829268293 - nodes in this community are weakly interconnected._