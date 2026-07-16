from app.extensions import ma
from app.models.team import Team


class TeamSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Team

    id = ma.auto_field(dump_only=True)
    nome = ma.auto_field(
        required=True,
        error_messages={"required": "Campo obrigatório"},
    )
