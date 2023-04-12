"""add user table

Revision ID: 9229ad7cd232
Revises: 5150b199e64e
Create Date: 2023-04-11 14:51:58.521499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9229ad7cd232'
down_revision = '5150b199e64e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass