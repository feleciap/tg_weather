from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from src.settings import DATABASE_URL, WEATHER_API_KEY
import logging
import requests

logging.basicConfig(level=logging.INFO)

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот для получения погоды, создан в качестве теста для компании BobrAi. Используйте команду /weather, чтобы узнать погоду.')

# Функция для получения данных о погоде
def get_weather(city: str):
    api_key = 'c477c9a4e60b398eaa5549590771bcb9'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Команда /weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Введите название города.')

# Функция для обработки текста от пользователя (название города)
async def handle_city_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city = update.message.text
    weather_data = get_weather(city)
    
    if weather_data is None or weather_data.get("cod") != 200:
        await update.message.reply_text("Не удалось найти город или получить данные о погоде. Попробуйте снова.")
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
    
    await update.message.reply_text(weather_message)

# Настройка бота с правильным токеном
application = ApplicationBuilder().token('7942737615:AAFmqToA_wFooi3Y5WkEmArKZsE9wL4To1k').build()

# Добавляем обработчики
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('weather', weather))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city_input))

if __name__ == '__main__':
    application.run_polling()
