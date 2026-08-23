"""Development entry point with concise startup logging."""

from app import create_app

app = create_app()


if __name__ == "__main__":
    settings = app.config["SETTINGS"]
    app.logger.info(
        "Starting %s | env=%s | http://127.0.0.1:%s",
        settings.app_name,
        settings.app_env,
        settings.app_port,
    )
    app.run(
        host="127.0.0.1",
        port=settings.app_port,
        debug=settings.app_env == "dev",
        use_reloader=settings.app_env == "dev",
    )

