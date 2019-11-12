"""Migracion anotacion 9

Revision ID: 1e67dec32b9b
Revises: 835dd6107d4f
Create Date: 2019-11-08 12:21:47.271778

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1e67dec32b9b'
down_revision = '835dd6107d4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tratamiento', sa.Column('color_primario', sa.Integer(), nullable=True))
    op.drop_constraint('tratamiento_ibfk_1', 'tratamiento', type_='foreignkey')
    op.create_foreign_key(None, 'tratamiento', 'color', ['color_primario'], ['id'])
    op.drop_column('tratamiento', 'color')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tratamiento', sa.Column('color', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'tratamiento', type_='foreignkey')
    op.create_foreign_key('tratamiento_ibfk_1', 'tratamiento', 'color', ['color'], ['id'])
    op.drop_column('tratamiento', 'color_primario')
    # ### end Alembic commands ###
