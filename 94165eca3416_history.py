"""Add bid_history, tender_history, bid_version

Revision ID: 94165eca3416
Revises: e913a1eee022
Create Date: 2024-09-13 19:54:09.970941

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "94165eca3416"
down_revision: Union[str, None] = "e913a1eee022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "bid_history",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("bid_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("tender_id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("creator_username", sa.String(length=100), nullable=False),
        sa.Column("version", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="bid_history_pkey"),
        sa.UniqueConstraint("bid_id", name="bid_history_bid_id_key"),
        sa.UniqueConstraint("organization_id", name="bid_history_organization_id_key"),
        sa.UniqueConstraint("tender_id", name="bid_history_tender_id_key"),
    )
    op.add_column(
        "bid_history",
        sa.Column(
            "status",
            sa.Enum(
                "Created",
                "Published",
                "Canceled",
                "Approved",
                "Rejected",
                name="bid_status",
            ),
            nullable=False,
        ),
    )

    op.create_table(
        "tender_history",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("tender_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("creator_username", sa.String(length=100), nullable=False),
        sa.Column("version", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("organization_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="tender_history_pkey"),
        sa.UniqueConstraint("tender_id", name="tender_history_tender_id_key"),
    )
    op.add_column(
        "tender_history",
        sa.Column(
            "service_type",
            sa.Enum(
                "Construction", "Delivery", "Manufacture", name="tender_service_type"
            ),
            nullable=False,
        ),
    )
    op.add_column(
        "tender_history",
        sa.Column(
            "status",
            sa.Enum("Created", "Published", "Closed", name="tender_status"),
            nullable=False,
        ),
    )
    op.add_column(
        "bid",
        sa.Column("version", sa.Integer(), server_default=sa.text("1"), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("bid", "version")
    op.drop_table("tender_history")
    op.drop_table("bid_history")
    # ### end Alembic commands ###
