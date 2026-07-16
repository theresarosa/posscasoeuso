from marshmallow import fields, validate

from app.extensions import ma
from app.models.participant import Participant


class ParticipantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Participant

    id = ma.auto_field(dump_only=True)
    nome = ma.auto_field(
        required=True,
        error_messages={"required": "Campo obrigatório"},
    )
    idade = fields.Integer(
        required=True,
        validate=validate.Range(min=1),
        error_messages={"required": "Campo obrigatório"},
    )
    team_id = ma.auto_field(
        required=True,
        error_messages={"required": "Campo obrigatório"},
    )
