from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    command = Column(String, nullable=False)
    request_time = Column(DateTime, default=datetime.utcnow)
    response = Column(String, nullable=False)
