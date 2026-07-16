from flask import Blueprint, jsonify, request

from app.controllers.user_controller import (
    atualizar_usuario,
    criar_usuario,
    deletar_usuario,
    listar_usuarios,
)
from app.utils.auth import token_required


users_bp = Blueprint("users", __name__)


@users_bp.route("/", methods=["GET"], strict_slashes=False)
def get_users():
    response, status = listar_usuarios()
    return jsonify(response), status


@users_bp.route("/", methods=["POST"], strict_slashes=False)
def post_user():
    data = request.get_json()
    response, status = criar_usuario(data)
    return jsonify(response), status


@users_bp.route("/<int:id>", methods=["PATCH"], strict_slashes=False)
@token_required
def patch_user(id):
    data = request.get_json()
    response, status = atualizar_usuario(id, data)
    return jsonify(response), status


@users_bp.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
@token_required
def delete_user(id):
    response, status = deletar_usuario(id)
    if status == 204:
        return "", 204
    return jsonify(response), status
