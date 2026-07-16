from flask import Blueprint, jsonify, request

from app.controllers.team_controller import (
    criar_equipe,
    listar_equipes,
    listar_participantes_por_equipe,
)
from app.utils.auth import token_required


teams_bp = Blueprint("teams", __name__)


@teams_bp.route("/", methods=["GET"], strict_slashes=False)
def get_teams():
    response, status = listar_equipes()
    return jsonify(response), status


@teams_bp.route("/", methods=["POST"], strict_slashes=False)
@token_required
def post_team():
    data = request.get_json()
    response, status = criar_equipe(data)
    return jsonify(response), status


@teams_bp.route("/<int:team_id>/participants", methods=["GET"], strict_slashes=False)
def get_team_participants(team_id):
    response, status = listar_participantes_por_equipe(team_id)
    return jsonify(response), status
