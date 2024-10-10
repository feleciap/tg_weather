import psycopg2

def get_logs():
    conn = psycopg2.connect("dbname=warehouse user=feleciap password=123")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"logs": "Все логи"}

def get_user_logs(user_id: int):
    conn = psycopg2.connect("dbname=warehouse user=feleciap password=123")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs WHERE user_id = %s", (user_id,))
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"user_logs": f"Логи для пользователя {user_id}"}
