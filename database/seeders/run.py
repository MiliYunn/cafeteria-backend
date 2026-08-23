"""Run all idempotent seeders in dependency order."""

from app import create_app
from database.seeders.admin_user import seed_admin_user
from database.seeders.payment_methods import seed_payment_methods
from database.seeders.roles import seed_roles


def run_seeders() -> None:
    app = create_app()
    with app.app_context():
        seed_roles()
        seed_payment_methods()
        seed_admin_user()
        app.logger.info("Database seeders completed")


if __name__ == "__main__":
    run_seeders()

