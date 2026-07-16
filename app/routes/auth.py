from flask import Blueprint, jsonify, request

from app.controllers.auth_controller import login


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def post_login():
    data = request.get_json()
    response, status = login(data)
    return jsonify(response), status
