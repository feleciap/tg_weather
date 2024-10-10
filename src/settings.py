import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройки для подключения к API
TELEGRAM_TOKEN = os.getenv('7942737615:AAFmqToA_wFooi3Y5WkEmArKZsE9wL4To1k')
WEATHER_API_KEY = os.getenv('c477c9a4e60b398eaa5549590771bcb9')  

# Настройки базы данных
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://feleciap:123@db_log:5432/warehouse')
