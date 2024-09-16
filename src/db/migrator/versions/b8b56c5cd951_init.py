"""Init

Revision ID: b8b56c5cd951
Revises: 
Create Date: 2024-09-16 04:26:04.375273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8b56c5cd951'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    op.create_table('bid_history',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('bid_id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Enum('Created', 'Published', 'Canceled', 'Approved', 'Rejected', name='bid_status'), nullable=False),
    sa.Column('tender_id', sa.Uuid(), nullable=False),
    sa.Column('author_type', sa.Enum('Organization', 'User', name='bid_author_type'), nullable=False),
    sa.Column('author_id', sa.Uuid(), nullable=False),
    sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('kvorum', sa.Integer(), nullable=False),
    sa.Column('votes_qty', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('decision', sa.Enum('Approved', 'Rejected', name='bid_decision'), nullable=True),
    sa.PrimaryKeyConstraint('id', name='bid_history_pkey')
    )
    op.create_table('employee',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id', name='employee_pkey'),
    sa.UniqueConstraint('username', name='employee_username_key')
    )
    op.create_table('organization',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('type', sa.Enum('IE', 'LLC', 'JSC', name='organization_type'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id', name='organization_pkey')
    )
    op.create_table('tender_history',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('tender_id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('service_type', sa.Enum('Construction', 'Delivery', 'Manufacture', name='tender_service_type'), nullable=False),
    sa.Column('status', sa.Enum('Created', 'Published', 'Closed', name='tender_status'), nullable=False),
    sa.Column('organization_id', sa.Uuid(), nullable=False),
    sa.Column('creator_username', sa.String(length=100), nullable=False),
    sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id', name='tender_history_pkey')
    )
    op.create_table('organization_responsible',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('organization_id', sa.Uuid(), nullable=True),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], name='organization_responsible_organization_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['employee.id'], name='organization_responsible_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='organization_responsible_pkey')
    )
    op.create_table('tender',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('service_type', sa.Enum('Construction', 'Delivery', 'Manufacture', name='tender_service_type'), nullable=False),
    sa.Column('status', sa.Enum('Created', 'Published', 'Closed', name='tender_status'), nullable=False),
    sa.Column('organization_id', sa.Uuid(), nullable=False),
    sa.Column('creator_username', sa.String(length=100), nullable=False),
    sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], name='tender_organization_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='tender_pkey')
    )
    op.create_table('bid',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Enum('Created', 'Published', 'Canceled', 'Approved', 'Rejected', name='bid_status'), nullable=False),
    sa.Column('tender_id', sa.Uuid(), nullable=False),
    sa.Column('author_type', sa.Enum('Organization', 'User', name='bid_author_type'), nullable=False),
    sa.Column('author_id', sa.Uuid(), nullable=False),
    sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('kvorum', sa.Integer(), nullable=False),
    sa.Column('votes_qty', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('decision', sa.Enum('Approved', 'Rejected', name='bid_decision'), nullable=True),
    sa.ForeignKeyConstraint(['tender_id'], ['tender.id'], name='bid_tender_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='bid_pkey')
    )
    op.create_table('feedback',
    sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('bid_id', sa.Uuid(), nullable=False),
    sa.Column('feedback', sa.Text(), nullable=False),
    sa.Column('creator_username', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['bid_id'], ['bid.id'], name='feedback_bid_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='feedback_pkey')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    op.drop_table('bid')
    op.drop_table('tender')
    op.drop_table('organization_responsible')
    op.drop_table('tender_history')
    op.drop_table('organization')
    op.drop_table('employee')
    op.drop_table('bid_history')
    op.execute('DROP TYPE IF EXISTS organization_type')
    op.execute('DROP TYPE IF EXISTS tender_status')
    op.execute('DROP TYPE IF EXISTS tender_service_type')
    op.execute('DROP TYPE IF EXISTS bid_status')
    op.execute('DROP TYPE IF EXISTS bid_decision')
    op.execute('DROP TYPE IF EXISTS bid_author_type')
    # ### end Alembic commands ###
