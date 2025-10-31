from __future__ import annotations
import os
from pathlib import Path

from sqlalchemy import create_engine

DATA_DIR = Path(os.getenv('VOCAB_DATA_DIR', 'data'))
DB_PATH = DATA_DIR / 'vocab.db'

_engine = None

def get_engine():
    """
    Return a singleton SQLAlchemy engine pointing to sqlite:///data/vocab.db.
    Ensures that the data directory exists.
    """
    global _engine
    if _engine is None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(f'sqlite:///{DB_PATH}', echo=False, future=True)
    return _engine

from app.core.models import Base

def init_db(drop: bool = False) -> None:
    """
    Create tables if missing. If drop= True, drop and recreate (dev only).
    """
    
    engine = get_engine()
    if drop:
        Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    
# add sessions
from contextlib import contextmanager
from typing import Iterator
from sqlalchemy.orm import Session, sessionmaker

_SessionLocal = None 

def get_sessionmaker() -> sessionmaker:
    global _SessionLocal
    if _SessionLocal is None:
        # create new Session objects 
        _SessionLocal = sessionmaker(bind = get_engine(), autoflush = False, autocommit = False, future = True)
    return _SessionLocal

@contextmanager
def session_scope() -> Iterator[Session]:
    """
    Provide a transactional scope around a series of operations.
    Usage:
        with session_scope() as s:
            s.add(Card())
            ...
    """
    SessionLocal = get_sessionmaker()
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    