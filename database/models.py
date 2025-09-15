from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
