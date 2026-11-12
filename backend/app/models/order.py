from sqlalchemy import String,Numeric,ForeignKey,Integer
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.core.database import Base
class Order(Base):
 __tablename__='orders'
 id:Mapped[int]=mapped_column(primary_key=True,index=True)
 user_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
 status:Mapped[str]=mapped_column(String(30),default='paid')
 payment_reference:Mapped[str]=mapped_column(String(80))
 total:Mapped[float]=mapped_column(Numeric(12,2))
 items:Mapped[list['OrderItem']]=relationship(back_populates='order',cascade='all, delete-orphan')
class OrderItem(Base):
 __tablename__='order_items'
 id:Mapped[int]=mapped_column(primary_key=True)
 order_id:Mapped[int]=mapped_column(ForeignKey('orders.id'))
 product_id:Mapped[int]=mapped_column(ForeignKey('products.id'))
 product_name:Mapped[str]=mapped_column(String(140))
 quantity:Mapped[int]=mapped_column(Integer)
 unit_price:Mapped[float]=mapped_column(Numeric(12,2))
 order:Mapped[Order]=relationship(back_populates='items')
