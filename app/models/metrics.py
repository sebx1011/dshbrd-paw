from psycopg import cursor
from datetime import date, timedelta
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


def get_invocaciones_lambdas(fecha_inicio=None, fecha_fin=None):
    conn = get_connection()
    cursor = conn.cursor()

    if fecha_inicio is None and fecha_fin is None:
        cursor.execute("""
                select l.lambda_name, sum(invocaciones) 
                from metrics as m 
                inner join lambdas as l 
                on m.lambda_id =l.id  
                group by(l.lambda_name)
            """)
    else:
        cursor.execute("""
            select l.lambda_name, sum(m.invocaciones)
            from metrics as m 
            inner join lambdas as l 
            on m.lambda_id =l.id
            where m.fecha between %s and %s
            group by(l.lambda_name) 
        """, (fecha_inicio, fecha_fin))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results


def get_tasa_exito(fecha_inicio=None, fecha_fin=None):
    conn = get_connection()
    cursor = conn.cursor()

    if fecha_inicio is None and fecha_fin is None:
        cursor.execute("""
            select l.lambda_name, sum(m.invocaciones), sum(m.errores) 
            from metrics as m 
            inner join lambdas as l 
            on m.lambda_id =l.id
            group by(l.lambda_name) 
        """)
    else:
        cursor.execute("""
            select l.lambda_name, sum(m.invocaciones), sum(m.errores) 
            from metrics as m 
            inner join lambdas as l 
            on m.lambda_id =l.id
            where m.fecha between %s and %s
            group by(l.lambda_name) 
        """, (fecha_inicio, fecha_fin))
    
    results = cursor.fetchall()
    for i in range(len(results)):
        lambda_name, invocaciones, errores = results[i]
        if invocaciones > 0:
            tasa_exito = round(((invocaciones - errores) / invocaciones) * 100, 2)
        else:
            tasa_exito = None
        results[i] = (lambda_name, tasa_exito)
    cursor.close()
    conn.close()
    
    return results