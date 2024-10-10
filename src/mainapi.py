from fastapi import FastAPI
from api.views import get_logs, get_user_logs  
from bot.logger import  log_request , logger
import logging

app = FastAPI()

@app.get("/logs")
def logs():
    return get_logs()

@app.get("/logs/{user_id}")
def user_logs(user_id: int):
    return get_user_logs(user_id)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="debug")
