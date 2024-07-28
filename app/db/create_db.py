from app.db.models.model import Base
from app.settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def create_db():
    settings = get_settings()
    engine: Engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)
    engine.connect()
