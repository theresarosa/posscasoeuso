from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.utils.response import success_response


user_schema = UserSchema()
users_schema = UserSchema(many=True)


def listar_usuarios():
    usuarios = User.query.all()
    return success_response(users_schema.dump(usuarios))


def criar_usuario(data):
    dados_validados = user_schema.load(data)
    dados_validados["senha"] = generate_password_hash(dados_validados["senha"])

    novo_usuario = User(**dados_validados)

    db.session.add(novo_usuario)
    db.session.commit()

    return success_response(user_schema.dump(novo_usuario), 201)


def atualizar_usuario(id, data):
    usuario = User.query.get_or_404(id)

    dados_validados = user_schema.load(data, partial=True)

    if "senha" in dados_validados:
        dados_validados["senha"] = generate_password_hash(dados_validados["senha"])

    for campo, valor in dados_validados.items():
        setattr(usuario, campo, valor)

    db.session.commit()

    return success_response(user_schema.dump(usuario))


def deletar_usuario(id):
    usuario = User.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return "", 204
