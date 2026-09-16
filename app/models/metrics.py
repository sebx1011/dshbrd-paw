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


def get_invocaciones_lambdas():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        select l.lambda_name, sum(invocaciones) 
        from metrics as m 
        inner join lambdas as l 
        on m.lambda_id =l.id  
        group by(l.lambda_name)
    """)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return results