"""create new schema, first alembic revision

Revision ID: cc180ca59bbd
Revises: 
Create Date: 2023-05-15 14:29:11.181226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc180ca59bbd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('starting_lbs', sa.BigInteger(), nullable=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('height_inches', sa.BigInteger(), nullable=True),
        sa.Column('avg_calorie_intake', sa.BigInteger(), nullable=True),
        sa.Column('age', sa.BigInteger(), nullable=True),
        sa.Column('gender', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('user_id', name='users_pkey')
    )

    op.create_table(
        'goals',
        sa.Column('goal_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('type_id', sa.BigInteger(), nullable=True),
        sa.Column('target_weight', sa.BigInteger(), nullable=True),
        sa.Column('workout_id', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('goal_id', name='goals_pkey')
    )

    op.create_table(
        'log',
        sa.Column('log_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('current_lbs', sa.BigInteger(), nullable=True),
        sa.Column('time_posted', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('log_id', name='log_pkey')
    )

    op.create_table(
        'workouts',
        sa.Column('workout_id', sa.BigInteger(), nullable=False),
        sa.Column('workout_name', sa.Text(), nullable=True),
        sa.Column('weight', sa.BigInteger(), nullable=True),
        sa.Column('distance_ft', sa.BigInteger(), nullable=True),
        sa.Column('repetitions', sa.BigInteger(), nullable=True),
        sa.Column('seconds', sa.BigInteger(), nullable=True),
        sa.Column('sets', sa.BigInteger(), nullable=True),
        sa.Column('times_per_week', sa.BigInteger(), nullable=True),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='workouts_user_id_fkey'),
        sa.PrimaryKeyConstraint('workout_id', name='workouts_pkey')
    )

    op.create_table(
        'goal_types',
        sa.Column('type_id', sa.BigInteger(), nullable=False),
        sa.Column('type', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('type_id', name='goal_types_pkey')
    )


def downgrade() -> None:
    op.drop_table('goal_types')
    op.drop_table('workouts')
    op.drop_table('log')
    op.drop_table('goals')
    op.drop_table('users')


