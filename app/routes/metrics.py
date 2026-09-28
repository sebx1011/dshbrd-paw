from flask import Blueprint
from app.models.metrics import get_invocaciones_lambdas
from app.models.metrics import get_tasa_exito
from app.services.tasa_biometria import calcular_tasa_biometria
from app.services.fecha_utils import calcular_rango_mes_anterior

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route('/metrics')
def metrics():
    fecha_inicio, fecha_fin = calcular_rango_mes_anterior()
    results = get_invocaciones_lambdas()
    tasa_exito = get_tasa_exito()
    results_mes_anterior = get_invocaciones_lambdas(fecha_inicio, fecha_fin)
    tasa_exito_mes_anterior = get_tasa_exito(fecha_inicio, fecha_fin)
    #convert result to a unique dictionary with lambda_name as key and sum(invocaciones) as value
    metrics_dict = {row[0]: row[1] for row in results}
    generate_invocaciones = metrics_dict["episodios-generarDocumentosPreAdmision-prod"]
    sign_invocaciones = metrics_dict["episodios-firmarDocumentosPreAdmision-prod"]

    results_mes_anterior_dict = {row[0]: row[1] for row in results_mes_anterior}
    tasa_exito_mes_anterior_dict = {row[0]: row[1] for row in tasa_exito_mes_anterior}

    tasa_biometria = calcular_tasa_biometria(generate_invocaciones, sign_invocaciones)

    exito_dict = {row[0]: row[1] for row in tasa_exito}
    return {
        "invocaciones": metrics_dict,
        "tasa_biometria": tasa_biometria,
        "tasa_exito": exito_dict,
        "ultimo_mes": {
            "invocaciones": results_mes_anterior_dict,
            "tasa_exito": tasa_exito_mes_anterior_dict
        }
    }, 200

