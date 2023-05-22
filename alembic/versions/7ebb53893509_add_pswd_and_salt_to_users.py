"""add pswd and salt to users

Revision ID: 7ebb53893509
Revises: 54db841c5205
Create Date: 2023-05-21 16:57:19.977684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ebb53893509'
down_revision = '54db841c5205'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('salt', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'password')
    op.drop_column('users', 'salt')
