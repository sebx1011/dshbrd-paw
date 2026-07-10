from flask import Blueprint, jsonify
from app.services.health_service import get_health_status

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health():
    health_status = get_health_status()
    return jsonify(health)
