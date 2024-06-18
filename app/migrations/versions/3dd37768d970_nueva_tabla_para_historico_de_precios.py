"""Nueva tabla para historico de precios

Revision ID: 3dd37768d970
Revises: 4c80d6068728
Create Date: 2024-06-15 11:41:19.613140

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3dd37768d970'
down_revision = '4c80d6068728'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_io_history',
       sa.Column('id', sa.Integer(), nullable=False),
       sa.Column('inventory_id', sa.Integer(), nullable=False),
       sa.Column('io_type', sa.Enum('IN', 'OUT', 'PRICE_UPDATE', name='io_type'), server_default='PRICE_UPDATE', nullable=False),
       sa.Column('quantity', sa.Integer(), server_default='0', nullable=False),
       sa.Column('price', sa.Numeric(precision=15, scale=5), server_default='0', nullable=False),
       sa.Column('transaction_date', sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
       sa.Column('created_at', sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
       sa.Column('updated_at', sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
       sa.ForeignKeyConstraint(['inventory_id'], ['product_inventory.id'], ),
       sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_io_history')
    # ### end Alembic commands ###