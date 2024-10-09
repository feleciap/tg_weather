from pydantic import BaseModel
from datetime import datetime

# Схема для логов
class LogSchema(BaseModel):
    user_id: int
    command: str
    request_time: datetime
    response: str

    class Config:
        orm_mode = True

# Схема для запроса погоды
class WeatherRequest(BaseModel):
    city: str
