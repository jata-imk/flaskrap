import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

class Config:
    APP_ENV = f'{os.getenv("APP_ENV")}'
    UPLOAD_FOLDER = f'{os.getenv("APP_STORAGE_FOLDER")}'
    
    SQLALCHEMY_ECHO=False
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    INERTIA_TEMPLATE = 'base.html'
    
