"""Turn log table into logs

Revision ID: 38a9dca01f68
Revises: c1e0267a981d
Create Date: 2023-05-24 17:22:08.334451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38a9dca01f68'
down_revision = 'c1e0267a981d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('log')
    op.create_table(
        'logs',
        sa.Column('log_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('current_lbs', sa.BigInteger(), nullable=True),
        sa.Column('time_posted', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('log_id', name='log_pkey')
    )
    op.drop_column('logs', 'log_id')
    op.add_column('logs', sa.Column('id', sa.Integer(), primary_key=True))


def downgrade() -> None:
    op.drop_table('logs')
    op.create_table(
        'log',
        sa.Column('log_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('current_lbs', sa.BigInteger(), nullable=True),
        sa.Column('time_posted', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('log_id', name='log_pkey')
    )
    op.drop_column('log', 'id')
    op.add_column('log', sa.Column('log_id', sa.BigInteger(), nullable=False))
