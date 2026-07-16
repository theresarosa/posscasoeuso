from werkzeug.security import check_password_hash

from app.models.user import User
from app.utils.auth import create_token
from app.utils.response import error_response, success_response


def login(data):
    if not data:
        return error_response("Dados inválidos", 400)

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return error_response("Email e senha são obrigatórios", 400)

    usuario = User.query.filter_by(email=email).first()

    if not usuario or not check_password_hash(usuario.senha, senha):
        return error_response("Credenciais inválidas", 401)

    token = create_token(usuario.id)
    return success_response({"token": token})
