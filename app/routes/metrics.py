from flask import Blueprint
from app.models.metrics import get_invocaciones_lambdas


metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route('/metrics')
def metrics():
    results = get_invocaciones_lambdas()
    #convert result to a unique dictionary with lambda_name as key and sum(invocaciones) as value
    metrics_dict = {row[0]: row[1] for row in results}
    return metrics_dict, 200
