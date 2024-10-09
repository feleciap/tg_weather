from telegram import Update 
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from bot.weather import get_weather
from bot.logger import log_request

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Логика получения погоды
    await update.message.reply_text("Вот ваша погода: ...")

weather_handler = CommandHandler('weather', get_weather)

async def weather(update: Update, context):
    if len(context.args) == 0:
        await update.message.reply_text("Пожалуйста, укажите город.")
        return
    
    city = ' '.join(context.args)
    weather_data = get_weather(city)
    
    if not weather_data:
        await update.message.reply_text("Не удалось найти город.")
        return
    
    response = (
        f"Погода в {city}:\nТемпература: {weather_data['temp']}°C\n"
        f"Ощущается как: {weather_data['feels_like']}°C\n"
        f"Описание: {weather_data['description']}\n"
        f"Влажность: {weather_data['humidity']}%\n"
        f"Скорость ветра: {weather_data['wind_speed']} м/с"
    )
    
    log_request(update.effective_user.id, city, response)
    await update.message.reply_text(response)

weather_handler = CommandHandler('weather', weather)
