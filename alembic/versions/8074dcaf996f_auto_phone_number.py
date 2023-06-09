"""auto-phone number

Revision ID: 8074dcaf996f
Revises: ec74d8965ae9
Create Date: 2023-04-12 15:22:52.673293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8074dcaf996f'
down_revision = 'ec74d8965ae9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
