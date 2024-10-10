import logging
import httpx
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from api.database import Log, get_db_session
from datetime import datetime
from src.settings import DATABASE_URL

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования для вывода в файл
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("app.log", mode='w'),  
        logging.StreamHandler()  
    ]
)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://feleciap:123@db_log:5432/warehouse')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'c477c9a4e60b398eaa5549590771bcb9')

if not WEATHER_API_KEY:
    logger.error("WEATHER_API_KEY не установлен. Проверьте .env файл")

def log_request(user_id: int, command: str, response: str):
    session = get_db_session()
    log_entry = Log(
        user_id=user_id,
        command=command,
        request_time=datetime.utcnow(),
        bot_response=response  
    )
    try:
        session.add(log_entry)
        session.commit()
        logger.info(f"Лог добавлен в базу данных для пользователя {user_id}")
    except Exception as e:
        logger.error("Ошибка при работе с базой данных: %s", e)
        session.rollback()  
    finally:
        session.close()