"""Atributo Corr y path

Revision ID: a887c0a14ba8
Revises: 1e67dec32b9b
Create Date: 2019-11-13 14:18:08.764901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a887c0a14ba8'
down_revision = '1e67dec32b9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('modulo', sa.Column('path', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('modulo', 'path')
    # ### end Alembic commands ###