import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URLs can be overridden via environment variables
LOG_DATABASE_URL = os.getenv("LOG_DATABASE_URL", "sqlite:///./log.db")
FEEDBACK_DATABASE_URL = os.getenv("FEEDBACK_DATABASE_URL", "sqlite:///./feedback.db")

log_engine = create_engine(LOG_DATABASE_URL, connect_args={"check_same_thread": False})
feedback_engine = create_engine(FEEDBACK_DATABASE_URL, connect_args={"check_same_thread": False})

engine = log_engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=log_engine)
FeedbackSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=feedback_engine)

Base = declarative_base()
FeedbackBase = declarative_base()


def init_log_db() -> None:
    from . import models 

    Base.metadata.create_all(bind=log_engine)


def init_feedback_db() -> None:
    from . import models  

    FeedbackBase.metadata.create_all(bind=feedback_engine)


def init_db() -> None:
    """Create tables for both databases."""
    init_log_db()
    init_feedback_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_feedback_db():
    db = FeedbackSessionLocal()
    try:
        yield db
    finally:
        db.close()