from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from pwdlib import PasswordHash
from app.core.config import settings
password_hash=PasswordHash.recommended()
def hash_password(value): return password_hash.hash(value)
def verify_password(value,hashed): return password_hash.verify(value,hashed)
def create_access_token(subject):
 exp=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
 return jwt.encode({'sub':subject,'exp':exp},settings.secret_key,algorithm='HS256')
def decode_access_token(token):
 try: return jwt.decode(token,settings.secret_key,algorithms=['HS256']).get('sub')
 except JWTError: return None
