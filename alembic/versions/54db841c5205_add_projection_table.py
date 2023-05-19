"""add projection table

Revision ID: 54db841c5205
Revises: 7f462fa3993b
Create Date: 2023-05-19 10:45:01.512912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54db841c5205'
down_revision = '7f462fa3993b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create projection table
    op.create_table(
        'projection',
        sa.Column('projection_id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id']),
        sa.Column('projection_date', sa.DateTime(), nullable=False),
        sa.Column('projection_lbs', sa.SmallInteger(), nullable=False),
        sa.Column('date_posted', sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    # Drop projection table
    op.drop_table('projection')
