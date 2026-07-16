"""cria tabelas teams e participants

Revision ID: 383c24114706
Revises: 
Create Date: 2026-04-23 10:27:38.732879

"""
from alembic import op
import sqlalchemy as sa


revision = '383c24114706'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('senha', sa.String(length=255), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('idade', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('participants')
    op.drop_table('teams')
    op.drop_table('users')
