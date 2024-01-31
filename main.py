import sentry_sdk
import logging
from sentry_sdk.integrations.logging import LoggingIntegration
from controllers.login_manager import AuthenticationAndPermissions
from settings import Base, ENGINE, DSN


def login():
    logging.basicConfig(level=logging.INFO)
    sentry_sdk.init(
        dsn=DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
        enable_tracing=True,
        debug=False,
        environment="development",
        integrations=[
            LoggingIntegration(
                level=logging.INFO,  # Capture info and above as breadcrumbs
                event_level=logging.INFO,  # Send records as events
            ),
        ],
    )

    Base.metadata.create_all(ENGINE)
    run = AuthenticationAndPermissions()
    run.check_password()


if __name__ == "__main__":
    login()
