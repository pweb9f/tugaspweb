import os
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey'  
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@localhost/toko_db'  
