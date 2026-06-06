# Basic
import asyncio

# CLI
from typer import Typer

# Application
from app.core.config import get_settings
from app.database.db_core import create_engine
from app.models.base_model import Base
import app.models  # noqa: F401


cli = Typer(
    help="Dev database utility tool",
    no_args_is_help=True,
)


@cli.command(help="Initialize the database by creating all tables")
def create_tables():
    get_settings().postgres_host = "localhost"
    engine = create_engine(get_settings().postgres_url)

    async def _create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully.")

    asyncio.run(_create_tables())


if __name__ == "__main__":
    cli()
