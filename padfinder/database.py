from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.expression import ClauseElement

from models import Base
from settings import DATABASE


@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations"""

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_or_create(session, model, defaults=None, **kwargs):
    """Return instance if it exists in the database, else create and return new
    instance"""

    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = {k: v for k, v in kwargs.items()
                  if not isinstance(v, ClauseElement)}

        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance


def connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE))


def create_tables(engine):
    Base.metadata.create_all(engine)
