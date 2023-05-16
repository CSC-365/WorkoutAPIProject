"""change from age to birthday

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
    # Modify the users table
    op.drop_column('users', 'age')
    op.add_column('users', sa.Column('birthday', sa.Date(), nullable=True))

    # Modify other tables as needed


def downgrade() -> None:
    # Modify the users table
    op.drop_column('users', 'birthday')
    op.add_column('users', sa.Column('age', sa.BigInteger(), nullable=True))

    # Modify other tables as needed
