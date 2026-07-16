from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, jsonify, request


def create_token(user_id):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "message": "Token não fornecido",
            }), 401

        token = auth_header.split(" ", 1)[1]
        try:
            jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return jsonify({
                "success": False,
                "message": "Token expirado",
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "success": False,
                "message": "Token inválido",
            }), 401

        return f(*args, **kwargs)

    return decorated
