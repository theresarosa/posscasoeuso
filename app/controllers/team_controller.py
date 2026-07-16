from app.extensions import db
from app.models.team import Team
from app.schemas.participant_schema import ParticipantSchema
from app.schemas.team_schema import TeamSchema
from app.utils.response import success_response


team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
participants_schema = ParticipantSchema(many=True)


def listar_equipes():
    equipes = Team.query.all()
    return success_response(teams_schema.dump(equipes))


def criar_equipe(data):
    dados_validados = team_schema.load(data)

    nova_equipe = Team(**dados_validados)

    db.session.add(nova_equipe)
    db.session.commit()

    return success_response(team_schema.dump(nova_equipe), 201)


def listar_participantes_por_equipe(team_id):
    team = Team.query.get_or_404(team_id)
    return success_response(participants_schema.dump(team.participants))
