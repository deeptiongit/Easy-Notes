from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_LOG_DATABASE_URL = 'sqlite:///./log.db'
SQLALCHEMY_FEEDBACK_DATABASE_URL = 'sqlite:///./feedback.db'

logsEngine = create_engine(SQLALCHEMY_LOG_DATABASE_URL, connect_args={
                       "check_same_thread": False})

feedbackEngine = create_engine(SQLALCHEMY_FEEDBACK_DATABASE_URL, connect_args={
                       "check_same_thread": False})


Base = declarative_base()

def get_logdb():
    SessionLocal = sessionmaker(bind=logsEngine, autocommit=False, autoflush=False,)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_feedbackdb():
    SessionLocal = sessionmaker(bind=feedbackEngine, autocommit=False, autoflush=False,)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()