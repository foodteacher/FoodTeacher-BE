"""add excess calories field

Revision ID: 0201baffc179
Revises: fb93d37d6676
Create Date: 2024-01-17 10:43:56.925767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0201baffc179'
down_revision: Union[str, None] = 'fb93d37d6676'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Exercise', sa.Column('excess_calories', sa.Float(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('Exercise', 'excess_calories')
    pass
