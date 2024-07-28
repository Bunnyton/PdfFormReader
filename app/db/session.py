from contextlib import contextmanager
from functools import lru_cache

from app.settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


@lru_cache()
def create_session() -> Session:
    settings = get_settings()

    engine: Engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    return Session()


@contextmanager
def get_session():
    session = create_session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def session_merge(session, object_, *filter_):  # for another fields
    res = session.query(object_.__class__).filter(*filter_).first()
    if not res:
        session.add(object_)
        res = object_

    return res
