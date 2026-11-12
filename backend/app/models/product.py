from sqlalchemy import String,Text,Numeric,Integer
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
class Product(Base):
 __tablename__='products'
 id:Mapped[int]=mapped_column(primary_key=True,index=True)
 name:Mapped[str]=mapped_column(String(140),index=True)
 description:Mapped[str]=mapped_column(Text,default='')
 price:Mapped[float]=mapped_column(Numeric(12,2))
 stock:Mapped[int]=mapped_column(Integer,default=0)
 category:Mapped[str]=mapped_column(String(80),default='General')
 image_url:Mapped[str]=mapped_column(String(500),default='')
