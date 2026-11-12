from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
 database_url:str='sqlite:///./ecommerce.db'
 secret_key:str='dev-only-change-this-secret'
 access_token_expire_minutes:int=60
 cors_origins:str='http://localhost:5173'
 model_config=SettingsConfigDict(env_file='.env',extra='ignore')
 @property
 def cors_origin_list(self): return [x.strip() for x in self.cors_origins.split(',') if x.strip()]
settings=Settings()
