from typing import List, Optional

from sqlalchemy import Column, DateTime, Enum, ForeignKeyConstraint, PrimaryKeyConstraint, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employee'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='employee_pkey'),
        UniqueConstraint('username', name='employee_username_key')
    )

    id = mapped_column(Uuid(as_uuid=True), server_default=text('uuid_generate_v4()'))
    username = mapped_column(String(50), nullable=False)
    first_name = mapped_column(String(50))
    last_name = mapped_column(String(50))
    created_at = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    organization_responsible: Mapped[List['OrganizationResponsible']] = relationship('OrganizationResponsible', uselist=True, back_populates='user')


class Organization(Base):
    __tablename__ = 'organization'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='organization_pkey'),
    )

    id = mapped_column(Uuid(as_uuid=True), server_default=text('uuid_generate_v4()'))
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(Text)
    type = mapped_column(Enum('IE', 'LLC', 'JSC', name='organization_type'))
    created_at = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    organization_responsible: Mapped[List['OrganizationResponsible']] = relationship('OrganizationResponsible', uselist=True, back_populates='organization')


class OrganizationResponsible(Base):
    __tablename__ = 'organization_responsible'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organization.id'], ondelete='CASCADE', name='organization_responsible_organization_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['employee.id'], ondelete='CASCADE', name='organization_responsible_user_id_fkey'),
        PrimaryKeyConstraint('id', name='organization_responsible_pkey')
    )

    id = mapped_column(Uuid(as_uuid=True), server_default=text('uuid_generate_v4()'))
    organization_id = mapped_column(Uuid)
    user_id = mapped_column(Uuid)

    organization: Mapped[Optional['Organization']] = relationship('Organization', back_populates='organization_responsible')
    user: Mapped[Optional['Employee']] = relationship('Employee', back_populates='organization_responsible')
