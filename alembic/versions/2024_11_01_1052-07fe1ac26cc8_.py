"""empty message

Revision ID: 07fe1ac26cc8
Revises: 137bf4460735
Create Date: 2024-11-01 10:52:10.864927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07fe1ac26cc8'
down_revision: Union[str, None] = '137bf4460735'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('registration_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client', 'registration_date')
    # ### end Alembic commands ###