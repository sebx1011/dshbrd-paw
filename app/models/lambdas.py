from database.connection import get_connection

def get_lambda(lambda_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM lambdas WHERE lambda_name = %s", (lambda_name,))
    lambda_data = cursor.fetchone()
    cursor.close()
    conn.close()
    if lambda_data is None:
        raise ValueError("Lambda not found")
    else:
        lambda_data = lambda_data[0]
    return lambda_data