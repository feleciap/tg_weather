import psycopg2

def get_logs():
    conn = psycopg2.connect("dbname=weather_logs user=postgres password=yourpassword")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return logs

def get_user_logs(user_id: int):
    conn = psycopg2.connect("dbname=weather_logs user=feleciap password=123")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs WHERE user_id = %s", (user_id,))
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return logs
