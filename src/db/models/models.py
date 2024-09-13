from typing import List, Optional

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class BidHistory(Base):
    __tablename__ = "bid_history"
    __table_args__ = (PrimaryKeyConstraint("id", name="bid_history_pkey"),)

    id = mapped_column(Uuid, server_default=text("uuid_generate_v4()"))
    bid_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(String, nullable=False)
    status = mapped_column(
        Enum(
            "Created",
            "Published",
            "Canceled",
            "Approved",
            "Rejected",
            name="bid_status",
        ),
        nullable=False,
    )
    tender_id = mapped_column(Uuid, nullable=False)
    organization_id = mapped_column(Uuid, nullable=False)
    creator_username = mapped_column(String(100), nullable=False)
    version = mapped_column(Integer, nullable=False, server_default=text("1"))
    description = mapped_column(Text)


class Employee(Base):
    __tablename__ = "employee"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="employee_pkey"),
        UniqueConstraint("username", name="employee_username_key"),
    )

    id = mapped_column(Uuid, server_default=text("uuid_generate_v4()"))
    username = mapped_column(String(50), nullable=False)
    first_name = mapped_column(String(50))
    last_name = mapped_column(String(50))
    created_at = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    organization_responsible: Mapped[List["OrganizationResponsible"]] = relationship(
        "OrganizationResponsible", uselist=True, back_populates="user"
    )


class Organization(Base):
    __tablename__ = "organization"
    __table_args__ = (PrimaryKeyConstraint("id", name="organization_pkey"),)

    id = mapped_column(Uuid, server_default=text("uuid_generate_v4()"))
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(Text)
    type = mapped_column(Enum("IE", "LLC", "JSC", name="organization_type"))
    created_at = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    organization_responsible: Mapped[List["OrganizationResponsible"]] = relationship(
        "OrganizationResponsible", uselist=True, back_populates="organization"
    )
    tender: Mapped[List["Tender"]] = relationship(
        "Tender", uselist=True, back_populates="organization"
    )
    bid: Mapped[List["Bid"]] = relationship(
        "Bid", uselist=True, back_populates="organization"
    )


class TenderHistory(Base):
    __tablename__ = "tender_history"
    __table_args__ = (PrimaryKeyConstraint("id", name="tender_history_pkey"),)

    id = mapped_column(Uuid, server_default=text("uuid_generate_v4()"))
    tender_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(String, nullable=False)
    service_type = mapped_column(
        Enum("Construction", "Delivery", "Manufacture", name="tender_service_type"),
        nullable=False,
    )
    status = mapped_column(
        Enum("Created", "Published", "Closed", name="tender_status"), nullable=False
    )
    creator_username = mapped_column(String(100), nullable=False)
    version = mapped_column(Integer, nullable=False, server_default=text("1"))
    description = mapped_column(Text)
    organization_id = mapped_column(Uuid)
    created_at = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class OrganizationResponsible(Base):
    __tablename__ = "organization_responsible"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
            ondelete="CASCADE",
            name="organization_responsible_organization_id_fkey",
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["employee.id"],
            ondelete="CASCADE",
            name="organization_responsible_user_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="organization_responsible_pkey"),
    )

    id = mapped_column(Uuid, server_default=text("uuid_generate_v4()"))
    organization_id = mapped_column(Uuid)
    user_id = mapped_column(Uuid)

    organization: Mapped[Optional["Organization"]] = relationship(
        "Organization", back_populates="organization_responsible"
    )
    user: Mapped[Optional["Employee"]] = relationship(
        "Employee", back_populates="organization_responsible"
    )


class Tender(Base):
    __tablename__ = "tender"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id"], ["organization.id"], name="tender_organization_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="tender_pkey"),
    )

    id = mapped_column(Uuid, server_default=text("uuid_generate_v4()"))
    name = mapped_column(String, nullable=False)
    service_type = mapped_column(
        Enum("Construction", "Delivery", "Manufacture", name="tender_service_type"),
        nullable=False,
    )
    status = mapped_column(
        Enum("Created", "Published", "Closed", name="tender_status"), nullable=False
    )
    creator_username = mapped_column(String(100), nullable=False)
    version = mapped_column(Integer, nullable=False, server_default=text("1"))
    description = mapped_column(Text)
    organization_id = mapped_column(Uuid)
    created_at = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    organization: Mapped[Optional["Organization"]] = relationship(
        "Organization", back_populates="tender"
    )
    bid: Mapped[List["Bid"]] = relationship(
        "Bid", uselist=True, back_populates="tender"
    )


class Bid(Base):
    __tablename__ = "bid"
    __table_args__ = (
        ForeignKeyConstraint(
            ["organization_id"], ["organization.id"], name="bid_organization_id_fkey"
        ),
        ForeignKeyConstraint(["tender_id"], ["tender.id"], name="bid_tender_id_fkey"),
        PrimaryKeyConstraint("id", name="bid_pkey"),
    )

    id = mapped_column(Uuid, server_default=text("uuid_generate_v4()"))
    name = mapped_column(String, nullable=False)
    status = mapped_column(
        Enum(
            "Created",
            "Published",
            "Canceled",
            "Approved",
            "Rejected",
            name="bid_status",
        ),
        nullable=False,
    )
    creator_username = mapped_column(String(100), nullable=False)
    description = mapped_column(Text)
    tender_id = mapped_column(Uuid)
    organization_id = mapped_column(Uuid)
    decision = mapped_column(Enum("Approved", "Rejected", name="bid_decision"))
    version = mapped_column(Integer, server_default=text("1"))

    organization: Mapped[Optional["Organization"]] = relationship(
        "Organization", back_populates="bid"
    )
    tender: Mapped[Optional["Tender"]] = relationship("Tender", back_populates="bid")
    feedback: Mapped[List["Feedback"]] = relationship(
        "Feedback", uselist=True, back_populates="bid"
    )


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = (
        ForeignKeyConstraint(
            ["bid_id"], ["bid.id"], ondelete="CASCADE", name="feedback_bid_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="feedback_pkey"),
    )

    id = mapped_column(Uuid, server_default=text("uuid_generate_v4()"))
    bid_id = mapped_column(Uuid, nullable=False)
    feedback = mapped_column(Text, nullable=False)
    creator_username = mapped_column(String(100), nullable=False)

    bid: Mapped["Bid"] = relationship("Bid", back_populates="feedback")
