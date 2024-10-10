import logging
import httpx
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from api.database import Log, get_db_session 
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваши настройки API
DATABASE_URL = os.getenv('DATABASE_URL')
WEATHER_API_KEY = os.getenv('c477c9a4e60b398eaa5549590771bcb9')

# Создание логов запросов в базу данных
def log_request(user_id: int, command: str, response: str):
    session = get_db_session()
    log_entry = Log(
        user_id=user_id,
        command=command,
        request_time=datetime.utcnow(),
        response=response
    )
    try:
        session.add(log_entry)
        session.commit()
    except Exception as e:
        logger.error("Database error: %s", e)
        session.rollback()  
    finally:
        session.close()

async def get_weather_data(city: str, user_id: int):
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Логируем успешный запрос
            log_request(user_id=user_id, command=f"Get weather for {city}", response=str(data))
            return data  # Возвращаем реальные данные о погоде
    except httpx.ConnectTimeout as e:
        logger.error("Connection timeout: %s", e)
        log_request(user_id=user_id, command=f"Get weather for {city}", response="Connection timeout")
        return {"error": "Connection timeout"}
    except httpx.HTTPStatusError as e:
        logger.error("HTTP error occurred: %s", e)
        log_request(user_id=user_id, command=f"Get weather for {city}", response=f"HTTP error: {e.response.status_code}")
        return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        logger.error("An error occurred: %s", e)
        log_request(user_id=user_id, command=f"Get weather for {city}", response=f"Error: {str(e)}")
        return {"error": str(e)}
