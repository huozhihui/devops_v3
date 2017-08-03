"""create table

Revision ID: cceb0603bca4
Revises: 
Create Date: 2017-07-19 16:08:12.538699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cceb0603bca4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('components',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('type', sa.String(length=20), nullable=True),
    sa.Column('version', sa.String(length=50), nullable=True),
    sa.Column('os', sa.String(length=50), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('homeworks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('inventory_updates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventorys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('hostid', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('brand', sa.String(length=50), nullable=True),
    sa.Column('asset_tag', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('used', sa.TEXT(), nullable=True),
    sa.Column('os', sa.String(length=50), nullable=True),
    sa.Column('os_short', sa.String(length=50), nullable=True),
    sa.Column('os_digits', sa.String(length=50), nullable=True),
    sa.Column('os_full', sa.TEXT(), nullable=True),
    sa.Column('mac_address', sa.String(length=50), nullable=True),
    sa.Column('serial_no', sa.String(length=50), nullable=True),
    sa.Column('host_networks', sa.TEXT(), nullable=True),
    sa.Column('host_netmask', sa.String(length=50), nullable=True),
    sa.Column('host_router', sa.String(length=50), nullable=True),
    sa.Column('oob_ip', sa.String(length=50), nullable=True),
    sa.Column('oob_netmask', sa.String(length=50), nullable=True),
    sa.Column('oob_router', sa.String(length=50), nullable=True),
    sa.Column('date_hw_purchase', sa.DATE(), nullable=True),
    sa.Column('date_hw_install', sa.DATE(), nullable=True),
    sa.Column('date_hw_expiry', sa.DATE(), nullable=True),
    sa.Column('date_hw_decomm', sa.DATE(), nullable=True),
    sa.Column('cabinet', sa.String(length=100), nullable=True),
    sa.Column('rack', sa.String(length=100), nullable=True),
    sa.Column('location', sa.TEXT(), nullable=True),
    sa.Column('department', sa.String(length=100), nullable=True),
    sa.Column('contact', sa.String(length=50), nullable=True),
    sa.Column('contact_tel', sa.String(length=50), nullable=True),
    sa.Column('contact_phone', sa.String(length=50), nullable=True),
    sa.Column('contact_email', sa.String(length=50), nullable=True),
    sa.Column('notes', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('zabbixs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('ip', sa.String(length=15), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('is_used', sa.Boolean(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ip')
    )
    op.create_table('hosts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('ip', sa.String(length=15), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('add_way', sa.String(length=10), nullable=True),
    sa.Column('notes', sa.TEXT(), nullable=True),
    sa.Column('inventory_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventorys.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ip')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('homework_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['homework_id'], ['homeworks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('upload_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('path', sa.String(length=100), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('component_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['component_id'], ['components.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('variables',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('value', sa.String(length=100), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('component_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['component_id'], ['components.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mid_task_components',
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('component_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['component_id'], ['components.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], )
    )
    op.create_table('mid_task_hosts',
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('host_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], )
    )
    op.create_table('mid_task_variables',
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('variable_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['variable_id'], ['variables.id'], )
    )
    op.create_table('task_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_results')
    op.drop_table('mid_task_variables')
    op.drop_table('mid_task_hosts')
    op.drop_table('mid_task_components')
    op.drop_table('variables')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('upload_files')
    op.drop_table('tasks')
    op.drop_table('hosts')
    op.drop_table('zabbixs')
    op.drop_table('roles')
    op.drop_table('inventorys')
    op.drop_table('inventory_updates')
    op.drop_table('homeworks')
    op.drop_table('components')
    # ### end Alembic commands ###
