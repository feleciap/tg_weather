from telegram.ext import ApplicationBuilder
from src.bot.handlers import weather_handler

application = ApplicationBuilder().token('7942737615:AAFmqToA_wFooi3Y5WkEmArKZsE9wL4To1k').build()

application.add_handler(weather_handler)

if __name__ == '__main__':
    application.run_polling()
