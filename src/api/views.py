import psycopg2
import logging

# Настраиваем логгер
logger = logging.getLogger(__name__)

def get_logs():

    conn = psycopg2.connect("dbname=warehouse user=feleciap password=123")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()
    logger.info(f"Logs fetched: {logs}") 
    cursor.close()
    conn.close()
       
    if logs:
        return {"logs": logs}  
    else:
        return {"message": "No logs found"}

def get_user_logs(user_id: int):

    conn = psycopg2.connect("dbname=warehouse user=feleciap password=123")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs WHERE user_id = %s", (user_id,))
    logs = cursor.fetchall()
    logger.info(f"Логи для пользователя {user_id} успешно получены: {logs}")    
    cursor.close()
    conn.close()

    return {"user_logs": logs} if logs else {"message": "Логи для пользователя не найдены"}