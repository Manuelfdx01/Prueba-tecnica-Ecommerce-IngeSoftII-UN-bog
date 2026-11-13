from sqlalchemy import select
from app.core.database import Base,engine,SessionLocal
from app.core.security import hash_password
from app.models import User,Product
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
 if not db.scalar(select(User).where(User.email=='admin@nexoshop.local')):
  db.add(User(name='Administrador',email='admin@nexoshop.local',hashed_password=hash_password('Admin123!'),role='admin'))
 if not db.scalar(select(Product.id).limit(1)):
  db.add_all([Product(name='Audífonos Studio',description='Sonido envolvente para tu día.',price=189900,stock=12,category='Tecnología',image_url='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=900'),Product(name='Reloj Minimal',description='Diseño limpio para cualquier ocasión.',price=129900,stock=8,category='Accesorios',image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=900'),Product(name='Mochila Urbana',description='Espacio y comodidad para moverte.',price=159900,stock=5,category='Accesorios',image_url='https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=900')])
 db.commit()
print('Datos demo listos.')
