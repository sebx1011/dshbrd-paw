from flask import Blueprint
from app.services.health_service import get_health_status

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health():
    health_status = get_health_status()
    if health_status["status"] == "healthy":
        return health_status, 200
    else:
        return health_status, 503
    