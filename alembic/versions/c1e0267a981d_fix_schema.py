"""fix schema

Revision ID: c1e0267a981d
Revises: 7ebb53893509
Create Date: 2023-05-21 18:39:55.594570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1e0267a981d'
down_revision = '7ebb53893509'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users', 'password')
    op.add_column('users', sa.Column(
        'password', sa.LargeBinary(), nullable=True))
    op.drop_column('users', 'salt')
    op.add_column('users', sa.Column('salt', sa.LargeBinary(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'password')
    op.drop_column('users', 'salt')
