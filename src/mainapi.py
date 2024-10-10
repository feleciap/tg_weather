from fastapi import FastAPI
from api.views import get_logs, get_user_logs  # Проверьте правильность импорта
from bot.logger import get_weather_data  # Проверьте правильность импорта

app = FastAPI()

@app.get("/logs")
def logs():
    return get_logs()

@app.get("/logs/{user_id}")
def user_logs(user_id: int):
    return get_user_logs(user_id)

@app.get("/weather/{city}")
async def weather(city: str, user_id: int):
    return await get_weather_data(city, user_id)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)