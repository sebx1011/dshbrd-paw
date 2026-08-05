from database.connection import get_connection
import psycopg

def get_health_status():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "healthy"}
    except psycopg.OperationalError:
        return {"status": "unhealthy"}