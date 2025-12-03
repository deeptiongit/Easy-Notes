from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from .database import Base, FeedbackBase

class Log(Base):
    __tablename__: str = 'Logs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    client_id = Column(Integer, ForeignKey('Clients.id'))

    handle = relationship("Client", back_populates="logs")


class Client(Base):
    __tablename__: str = 'Clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    logs = relationship('Log', back_populates="handle")


class FeedbackData(FeedbackBase):
    __tablename__ = "feedback_data"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String, index=True)
    ocr_text = Column(Text)
    doc_type = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
