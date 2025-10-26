from __future__ import annotations
from datetime import datetime, date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Date, DateTime, ForeignKey, Index, func

# Base class every model will inherit from
class Base(DeclarativeBase):
    pass

class Card(Base):
    __tablename__ = 'cards'
    
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    de: Mapped[str] = mapped_column(String, nullable = False) # German
    en: Mapped[str] = mapped_column(String, nullable = False) # English
    tags: Mapped[str | None] = mapped_column(String, nullable = True) # optional, comma-separated tags
    
    # Spaced repetition fields
    ease_factor: Mapped[float] = mapped_column(Float, nullable = False, default = 2.5)
    inteval_days: Mapped[int] = mapped_column(Integer, nullable = False, default = 0)
    reps: Mapped[int] = mapped_column(Integer, nullable = False, default = 0)
    lapses: Mapped[int] = mapped_column(Integer, nullable = False, default = 0)
    due_date: Mapped[date | None] = mapped_column(Date, nullable = True)
    last_reviewed: Mapped[datetime | None] = mapped_column(DateTime, nullable = True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable = False, server_default = func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable = False, server_default = func.current_timestamp(), onupdate = func.current_timestamp())
    
    # Helpful indexes
    __table_args__ =    (
        Index('ix_cards_due_date', 'due_date'),
        Index('ix_cards_de_en', 'de', 'en')
    )