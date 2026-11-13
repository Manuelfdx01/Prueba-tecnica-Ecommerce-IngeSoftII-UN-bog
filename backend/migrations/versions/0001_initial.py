"""Initial schema for NexoShop."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
revision='0001_initial'
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
 # Compatibility: the first prototype created these tables with metadata.create_all.
 # If that schema already exists, record the baseline instead of recreating it.
 if inspect(op.get_bind()).has_table('users'):
  return
 op.create_table('users',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('name',sa.String(100),nullable=False),sa.Column('email',sa.String(255),nullable=False),sa.Column('hashed_password',sa.String(255),nullable=False),sa.Column('role',sa.String(20),nullable=False,server_default='customer'))
 op.create_index('ix_users_id','users',['id']); op.create_index('ix_users_email','users',['email'],unique=True)
 op.create_table('products',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('name',sa.String(140),nullable=False),sa.Column('description',sa.Text(),nullable=False,server_default=''),sa.Column('price',sa.Numeric(12,2),nullable=False),sa.Column('stock',sa.Integer(),nullable=False,server_default='0'),sa.Column('category',sa.String(80),nullable=False,server_default='General'),sa.Column('image_url',sa.String(500),nullable=False,server_default=''))
 op.create_index('ix_products_id','products',['id']); op.create_index('ix_products_name','products',['name'])
 op.create_table('orders',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('user_id',sa.Integer(),sa.ForeignKey('users.id'),nullable=False),sa.Column('status',sa.String(30),nullable=False,server_default='paid'),sa.Column('payment_reference',sa.String(80),nullable=False),sa.Column('total',sa.Numeric(12,2),nullable=False))
 op.create_index('ix_orders_id','orders',['id'])
 op.create_table('order_items',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('order_id',sa.Integer(),sa.ForeignKey('orders.id'),nullable=False),sa.Column('product_id',sa.Integer(),sa.ForeignKey('products.id'),nullable=False),sa.Column('product_name',sa.String(140),nullable=False),sa.Column('quantity',sa.Integer(),nullable=False),sa.Column('unit_price',sa.Numeric(12,2),nullable=False))
def downgrade():
 op.drop_table('order_items'); op.drop_index('ix_orders_id',table_name='orders'); op.drop_table('orders'); op.drop_index('ix_products_name',table_name='products'); op.drop_index('ix_products_id',table_name='products'); op.drop_table('products'); op.drop_index('ix_users_email',table_name='users'); op.drop_index('ix_users_id',table_name='users'); op.drop_table('users')
