"""add content column in post table

Revision ID: 5150b199e64e
Revises: 2f7a9a77ac08
Create Date: 2023-04-11 14:47:44.424669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5150b199e64e'
down_revision = '2f7a9a77ac08'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass