from app.extensions import db


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    participants = db.relationship(
        "Participant",
        backref="team",
        lazy=True,
        cascade="all, delete-orphan",
    )
