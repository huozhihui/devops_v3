"""add alias to inventory

Revision ID: 4d968a25d137
Revises: baadaf5b3851
Create Date: 2017-08-10 10:50:57.156848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d968a25d137'
down_revision = 'baadaf5b3851'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventorys', sa.Column('alias_name', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inventorys', 'alias_name')
    # ### end Alembic commands ###
