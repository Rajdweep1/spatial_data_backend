import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:admin@127.0.0.1:3306/spatial_backend"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
