from flask import Flask
from marshmallow import ValidationError
from http.client import HTTPException

from .config import Config
from .extensions import db, ma, migrate
from .routes.auth import auth_bp
from .routes.participants import participants_bp
from .routes.teams import teams_bp
from .routes.users import users_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from .models import participant, team, user  # noqa: F401

    app.register_blueprint(auth_bp)
    app.register_blueprint(teams_bp, url_prefix="/teams")
    app.register_blueprint(participants_bp, url_prefix="/participants")
    app.register_blueprint(users_bp, url_prefix="/users")

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return {"success": False, "errors": err.messages}, 400

    @app.errorhandler(404)
    def handle_404(err):
        return {"success": False, "message": "Recurso não encontrado"}, 404

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        if isinstance(e, HTTPException):
            return e
        return {"success": False, "message": "Erro interno do servidor"}, 500

    return app
