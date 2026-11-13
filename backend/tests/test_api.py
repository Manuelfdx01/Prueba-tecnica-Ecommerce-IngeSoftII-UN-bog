from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy import select
from app.main import app
from app.core.database import SessionLocal
from app.models import User,Product
from app.core.security import hash_password
client=TestClient(app)
def test_register_login_and_customer_permissions():
 email=f'test-{uuid4().hex[:8]}@example.com'
 r=client.post('/api/auth/register',json={'name':'Test User','email':email,'password':'password123'})
 assert r.status_code==201
 assert r.json()['role']=='customer'
 login=client.post('/api/auth/login',data={'username':email,'password':'password123'})
 assert login.status_code==200
 token=login.json()['access_token']
 assert client.get('/api/auth/me',headers={'Authorization':f'Bearer {token}'}).status_code==200
 assert client.post('/api/products',headers={'Authorization':f'Bearer {token}'},json={'name':'Blocked','price':10,'stock':1}).status_code==403

def test_checkout_rejects_insufficient_stock_and_preserves_stock():
 email=f'buyer-{uuid4().hex[:8]}@example.com'
 with SessionLocal() as db:
  user=User(name='Buyer',email=email,hashed_password=hash_password('password123'),role='customer')
  product=Product(name='Test stock item',description='test',price=1000,stock=1,category='Test',image_url='')
  db.add_all([user,product]);db.commit();uid=user.id;pid=product.id
 token=client.post('/api/auth/login',data={'username':email,'password':'password123'}).json()['access_token']
 headers={'Authorization':f'Bearer {token}'}
 response=client.post('/api/orders/checkout',headers=headers,json={'items':[{'product_id':pid,'quantity':2}]})
 assert response.status_code==409
 with SessionLocal() as db: assert db.get(Product,pid).stock==1
 response=client.post('/api/orders/checkout',headers=headers,json={'items':[{'product_id':pid,'quantity':1}]})
 assert response.status_code==201
 assert response.json()['total']=='1000.00'
 with SessionLocal() as db: assert db.get(Product,pid).stock==0
