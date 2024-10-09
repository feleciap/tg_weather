import logging
import httpx
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from api.database import Log, get_db_session  # Убедитесь, что у вас есть эта модель
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
    session.add(log_entry)
    session.commit()
    session.close()

async def get_weather_data(city, user_id: int):
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = response.json()  # Возвращаем ответ в формате JSON
            
            # Логируем успешный запрос
            log_request(user_id=user_id, command=f"Get weather for {city}", response=str(data))
            return data
    except httpx.ConnectTimeout as e:
        logger.error("Connection timeout: %s", e)
        log_request(user_id=user_id, command=f"Get weather for {city}", response="Connection timeout")
        return None
    except httpx.HTTPStatusError as e:
        logger.error("HTTP error occurred: %s", e)
        log_request(user_id=user_id, command=f"Get weather for {city}", response=f"HTTP error: {e.response.status_code}")
        return None
    except Exception as e:
        logger.error("An error occurred: %s", e)
        log_request(user_id=user_id, command=f"Get weather for {city}", response=f"Error: {str(e)}")
        return None

# Пример вызова функции
async def main():
    user_id = 123  # Замените на ID пользователя, который выполняет запрос
    city = "Moscow"  # Замените на нужный вам город
    weather_data = await get_weather_data(city, user_id)
    if weather_data:
        logger.info("Weather data retrieved: %s", weather_data)
    else:
        logger.warning("Failed to retrieve weather data.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
