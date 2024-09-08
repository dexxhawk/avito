"""Init migration. Add employee, organization, organization_responsible

Revision ID: a96b09013a66
Revises: 
Create Date: 2024-09-08 19:10:22.027454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a96b09013a66'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id', name='employee_pkey'),
    sa.UniqueConstraint('username', name='employee_username_key')
    )
    op.create_table('organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('type', sa.Enum('IE', 'LLC', 'JSC', name='organization_type'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id', name='organization_pkey')
    )
    op.create_table('organization_responsible',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], name='organization_responsible_organization_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['employee.id'], name='organization_responsible_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='organization_responsible_pkey')
    )


def downgrade() -> None:
    op.drop_table('organization_responsible')
    op.drop_table('organization')
    op.drop_table('employee')
    op.execute('DROP TYPE IF EXISTS organization_type')
