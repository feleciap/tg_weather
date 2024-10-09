from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.settings import DATABASE_URL

# Настройка подключения к базе данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модель логов запросов
class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    command = Column(String, nullable=False)
    request_time = Column(DateTime, default=datetime.utcnow)
    response = Column(String, nullable=False)

# Создание сессии для работы с базой данных
def get_db_session():
    return SessionLocal()

# Инициализация базы данных
def init_db():
    Base.metadata.create_all(bind=engine)
