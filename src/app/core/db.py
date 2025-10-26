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
    
    