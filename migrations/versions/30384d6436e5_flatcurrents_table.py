"""flatcurrents table

Revision ID: 30384d6436e5
Revises: c2b1cf3ab0cc
Create Date: 2020-08-20 00:13:27.789538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30384d6436e5'
down_revision = 'c2b1cf3ab0cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flatcurrent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=240), nullable=True),
    sa.Column('district', sa.String(length=64), nullable=True),
    sa.Column('roomsNo', sa.String(length=64), nullable=True),
    sa.Column('size', sa.String(length=64), nullable=True),
    sa.Column('price', sa.String(length=64), nullable=True),
    sa.Column('pricePerM2', sa.String(length=64), nullable=True),
    sa.Column('link', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flatcurrent_district'), 'flatcurrent', ['district'], unique=False)
    op.create_index(op.f('ix_flatcurrent_title'), 'flatcurrent', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_flatcurrent_title'), table_name='flatcurrent')
    op.drop_index(op.f('ix_flatcurrent_district'), table_name='flatcurrent')
    op.drop_table('flatcurrent')
    # ### end Alembic commands ###