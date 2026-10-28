from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self):
        settings = get_settings()

        self.engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

        self.session_factory = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False
        )

    def get_session(self):
        with self.session_factory() as session:
            yield session

    def check_connection(self):
        with self.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return True


database = Database()
