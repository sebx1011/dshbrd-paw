from database.connection import get_connection
from app.models.lambdas import get_lambda

def upsert_metrics(lambda_name, fecha, invocaciones, errores):

    lambda_id = get_lambda(lambda_name)  # Check if the lambda exists, raises ValueError if not

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO metrics (lambda_id, fecha, invocaciones, errores, updated_at)
        VALUES (%s, %s, %s, %s, NOW())
        ON CONFLICT (lambda_id, fecha) DO UPDATE SET
            invocaciones = EXCLUDED.invocaciones,
            errores = EXCLUDED.errores,
            updated_at = EXCLUDED.updated_at
    """, (lambda_id, fecha, invocaciones, errores))
    cursor.close()
    conn.commit()
    conn.close()