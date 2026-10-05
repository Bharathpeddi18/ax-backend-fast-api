import os

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


load_dotenv()


config = context.config

target_metadata = None


def get_database_url():
    return URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("AZURE_DB_USER"),
        password=os.getenv("AZURE_DB_PASSWORD"),
        host=os.getenv("AZURE_DB_HOST"),
        port=int(os.getenv("AZURE_DB_PORT", "5432") or "5432"),
        database=os.getenv("AZURE_DB_NAME"),
        query={
            "sslmode": os.getenv(
                "AZURE_DB_SSLMODE",
                "disable",
            )
        },
    )


def run_migrations_offline():
    url = get_database_url()

    context.configure(
        url=url.render_as_string(
            hide_password=False
        ),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(
        get_database_url()
    )

    with engine.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()