from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from bot.database import Log, get_db_session
from datetime import datetime

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
