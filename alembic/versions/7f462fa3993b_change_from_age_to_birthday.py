"""change from age to birthday & auto generate ids

Revision ID: 7f462fa3993b
Revises: cc180ca59bbd
Create Date: 2023-05-16 10:26:02.926803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f462fa3993b'
down_revision = 'cc180ca59bbd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # age -> birthday
    op.drop_column('users', 'age')
    op.add_column('users', sa.Column('birthday', sa.Date(), nullable=True))

    # Auto generate ids
    op.drop_column('users', 'user_id')
    op.add_column('users', sa.Column('id', sa.Integer(), primary_key=True))

    # Auto generate ids for goals table
    op.drop_column('goals', 'goal_id')
    op.add_column('goals', sa.Column('id', sa.Integer(), primary_key=True))

    # Auto generate ids for workouts table
    op.drop_column('workouts', 'workout_id')
    op.add_column('workouts', sa.Column('id', sa.Integer(), primary_key=True))


def downgrade() -> None:
    # age -> birthday
    op.drop_column('users', 'birthday')
    op.add_column('users', sa.Column('age', sa.BigInteger(), nullable=True))

    # Auto generate ids
    op.drop_column('users', 'id')
    op.add_column('users', sa.Column(
        'user_id', sa.BigInteger(), nullable=False))

    # Auto generate ids for goals table
    op.drop_column('goals', 'id')
    op.add_column('goals', sa.Column(
        'goal_id', sa.BigInteger(), nullable=False))

    # Auto generate ids for workouts table
    op.drop_column('workouts', 'id')
    op.add_column('workouts', sa.Column(
        'workout_id', sa.BigInteger(), nullable=False))
