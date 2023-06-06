"""lil turn big

Revision ID: 4b51e35ebf68
Revises: 38cd076a2f51
Create Date: 2023-06-06 03:23:32.042790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b51e35ebf68'
down_revision = '38cd076a2f51'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('projection', 'projection_lbs', type_=sa.BigInteger())


def downgrade() -> None:
    op.alter_column('projection', 'projection_lbs', type_=sa.SmallInteger())
