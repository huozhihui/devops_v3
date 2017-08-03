"""add host_groups table

Revision ID: ef9105e6f4ac
Revises: 820ec5df2fbb
Create Date: 2017-08-02 16:03:45.249694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef9105e6f4ac'
down_revision = '820ec5df2fbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('host_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('groupid', sa.Integer(), nullable=True),
    sa.Column('notes', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('host_groups')
    # ### end Alembic commands ###
