"""add_tables

Revision ID: 9fbbacb8230d
Revises: 0201baffc179
Create Date: 2024-01-27 15:03:26.318438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision: str = '9fbbacb8230d'
down_revision: Union[str, None] = '0201baffc179'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserDietPlanInfoV2',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('advice', sa.Text(), nullable=True),
    sa.Column('recommended_exercise', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    )
    
    op.create_table('MenusV2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_diet_plan_info_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('calories', sa.Float(), nullable=True),
    sa.Column('car', sa.Float(), nullable=True),
    sa.Column('pro', sa.Float(), nullable=True),
    sa.Column('fat', sa.Float(), nullable=True),
    sa.Column('meal_time', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['user_diet_plan_info_id'], ['UserDietPlanInfoV2.id'], ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    insp = reflection.Inspector.from_engine(op.get_bind())
    if 'MenusV2' in insp.get_table_names():
        op.drop_table('MenusV2')
    if 'UserDietPlanInfoV2' in insp.get_table_names():
        op.drop_table('UserDietPlanInfoV2')
    # ### end Alembic commands ###
