from flask import Blueprint, jsonify, request

from app.controllers.participant_controller import criar_participante, listar_participantes
from app.utils.auth import token_required


participants_bp = Blueprint("participants", __name__)


@participants_bp.route("/", methods=["GET"], strict_slashes=False)
def get_participants():
    response, status = listar_participantes()
    return jsonify(response), status


@participants_bp.route("/", methods=["POST"], strict_slashes=False)
@token_required
def post_participant():
    data = request.get_json()
    response, status = criar_participante(data)
    return jsonify(response), status
