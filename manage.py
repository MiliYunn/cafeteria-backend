"""Unified command runner for APCafeteria backend development tasks."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def run_command(arguments: Sequence[str]) -> int:
    """Run a project command with the current Python interpreter."""
    command = [sys.executable, *arguments]
    print(f"> {' '.join(command)}", flush=True)
    completed = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage the APCafeteria API, database migrations, and seed data.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("run", help="Start the Flask development server.")
    subparsers.add_parser("seed", help="Run all idempotent database seeders.")
    subparsers.add_parser("test", help="Run the pytest test suite.")

    migrate = subparsers.add_parser("migrate", help="Upgrade the database schema.")
    migrate.add_argument("revision", nargs="?", default="head", help="Target revision (default: head).")
    migrate.add_argument("--sql", action="store_true", help="Print SQL without changing the database.")

    downgrade = subparsers.add_parser("downgrade", help="Downgrade the database schema.")
    downgrade.add_argument("revision", nargs="?", default="-1", help="Target revision (default: -1).")
    downgrade.add_argument("--sql", action="store_true", help="Print SQL without changing the database.")

    revision = subparsers.add_parser("revision", help="Create a new Alembic revision.")
    revision.add_argument("message", help="Short migration description.")
    revision.add_argument(
        "--autogenerate",
        action="store_true",
        help="Generate operations by comparing models with the connected database.",
    )

    subparsers.add_parser("current", help="Show the database's current Alembic revision.")
    subparsers.add_parser("history", help="Show Alembic revision history.")
    subparsers.add_parser("heads", help="Show available Alembic heads.")

    stamp = subparsers.add_parser("stamp", help="Stamp a revision without running migrations.")
    stamp.add_argument("revision", nargs="?", default="head", help="Revision to stamp (default: head).")

    return parser


def dispatch(args: argparse.Namespace) -> int:
    if args.command == "run":
        return run_command(["run.py"])
    if args.command == "seed":
        return run_command(["-m", "database.seeders.run"])
    if args.command == "test":
        return run_command(["-m", "pytest", "-q"])
    if args.command == "migrate":
        command = ["-m", "alembic", "upgrade", args.revision]
        if args.sql:
            command.append("--sql")
        return run_command(command)
    if args.command == "downgrade":
        command = ["-m", "alembic", "downgrade", args.revision]
        if args.sql:
            command.append("--sql")
        return run_command(command)
    if args.command == "revision":
        command = ["-m", "alembic", "revision", "-m", args.message]
        if args.autogenerate:
            command.append("--autogenerate")
        return run_command(command)
    if args.command in {"current", "history", "heads"}:
        return run_command(["-m", "alembic", args.command])
    if args.command == "stamp":
        return run_command(["-m", "alembic", "stamp", args.revision])
    raise ValueError(f"Unsupported command: {args.command}")


def main() -> int:
    return dispatch(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())

