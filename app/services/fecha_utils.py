from datetime import date, timedelta


def calcular_rango_mes_anterior():
    today = date.today()
    primer_dia_del_mes = today.replace(day=1)
    ultimo_dia_del_mes_anterior = today.replace(day=1) - timedelta(days=1)
    primer_dia_del_mes_anterior = ultimo_dia_del_mes_anterior.replace(day=1)

    return primer_dia_del_mes_anterior, ultimo_dia_del_mes_anterior
