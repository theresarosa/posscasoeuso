from app.extensions import db


class Participant(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
