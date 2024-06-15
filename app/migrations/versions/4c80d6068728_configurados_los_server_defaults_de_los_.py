"""Configurados los server_defaults de los modelos y agregado sku en product_inventory

Revision ID: 4c80d6068728
Revises: 8be928e8688f
Create Date: 2024-06-14 17:42:00.467147

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4c80d6068728"
down_revision = "8be928e8688f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("product", schema=None) as batch_op:
        batch_op.alter_column(
            "name",
            existing_type=sa.String(length=127),
            nullable=False,
            server_default="",
        )

        batch_op.alter_column(
            "description",
            existing_type=sa.String(length=255),
            nullable=False,
            server_default="",
        )

        batch_op.alter_column(
            "small_image",
            existing_type=sa.String(length=127),
            nullable=False,
            server_default="",
        )

        batch_op.alter_column(
            "out_of_stock",
            existing_type=sa.Boolean(),
            nullable=False,
            server_default="1",
        )

        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        )

        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        )

    with op.batch_alter_table("brand", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        )

    with op.batch_alter_table("category", schema=None) as batch_op:
        batch_op.alter_column(
            "description",
            existing_type=sa.String(length=255),
            nullable=False,
            server_default="",
        )

    with op.batch_alter_table("product_inventory", schema=None) as batch_op:
        batch_op.alter_column(
            "price",
            existing_type=sa.Numeric(precision=15, scale=5),
            nullable=False,
            server_default="0",
        )

        batch_op.alter_column(
            "quantity",
            existing_type=sa.Integer(),
            nullable=False,
            server_default="0",
        )

        batch_op.alter_column(
            "creation_date",
            existing_type=sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            new_column_name="created_at",
        )

        batch_op.alter_column(
            "modified_date",
            existing_type=sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            new_column_name="updated_at",
        )

        batch_op.add_column(
            sa.Column("sku", sa.String(length=63), server_default="", nullable=False)
        )

    with op.batch_alter_table("vendor", schema=None) as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        )
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("product", schema=None) as batch_op:
        batch_op.alter_column("name", server_default=None)
        batch_op.alter_column("description", server_default=None)
        batch_op.alter_column("small_image", server_default=None)
        batch_op.alter_column("out_of_stock", server_default=None)
        batch_op.alter_column("created_at", existing_type=sa.DateTime(), nullable=False)
        batch_op.alter_column("updated_at", existing_type=sa.DateTime(), nullable=False)

    with op.batch_alter_table("brand", schema=None) as batch_op:
        batch_op.alter_column("created_at", existing_type=sa.DateTime(), nullable=False)
        batch_op.alter_column("updated_at", existing_type=sa.DateTime(), nullable=False)

    with op.batch_alter_table("category", schema=None) as batch_op:
        batch_op.alter_column("description", server_default=None)

    with op.batch_alter_table("brand", schema=None) as batch_op:
        batch_op.alter_column("created_at", existing_type=sa.DateTime(), nullable=False)
        batch_op.alter_column("updated_at", existing_type=sa.DateTime(), nullable=False)

    with op.batch_alter_table("product_inventory", schema=None) as batch_op:
        batch_op.alter_column("price", server_default=None)
        batch_op.alter_column("quantity", server_default=None)

        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=False,
            new_column_name="creation_date",
        )

        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            nullable=False,
            new_column_name="modified_date",
        )

        batch_op.drop_column("sku")

    with op.batch_alter_table("vendor", schema=None) as batch_op:
        batch_op.alter_column("created_at", existing_type=sa.DateTime(), nullable=False)
        batch_op.alter_column("updated_at", existing_type=sa.DateTime(), nullable=False)

    # ### end Alembic commands ###
