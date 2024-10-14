import logging
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram import F
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение токенов из окружения
API_TOKEN = os.getenv('API_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# Логирование
logging.basicConfig(level=logging.DEBUG)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, timeout=20)
dp = Dispatcher()

# Асинхронная функция для получения данных о погоде
async def get_weather(city: str):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_message = (await response.json()).get("message", "Неизвестная ошибка")
                    print(f"Ошибка: {error_message}")
                    return None
        except aiohttp.ClientError as e:
            print(f"Ошибка HTTP: {e}")
            return None
        except asyncio.TimeoutError:
            print("Превышено время ожидания запроса")
            return None

# Обработка команды /start
@dp.message(F.text == "/start")
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот для получения погоды, создан в качестве теста для компании BobrAi. Используйте команду /weather, чтобы узнать погоду.")

# Обработка команды /weather
@dp.message(F.text == "/weather")
async def ask_city(message: types.Message):
    await message.answer("Введите название города.")

# Обработка текстовых сообщений (название города)
@dp.message(F.text)
async def handle_city_input(message: types.Message):
    city = message.text.strip()
    weather_data = await get_weather(city)
    
    if weather_data is None or weather_data.get("cod") != 200:
        await message.answer("Не удалось найти город или получить данные о погоде. Попробуйте снова.")
        return
    
    description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']

    weather_message = (
        f"Погода в городе {city}:\n"
        f"Температура: {temperature}°C\n"
        f"Ощущается как: {feels_like}°C\n"
        f"Описание: {description}\n"
        f"Влажность: {humidity}%\n"
        f"Скорость ветра: {wind_speed} м/с"
    )
    
    await message.answer(weather_message)

# Основная функция запуска
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
