from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
import os

db = SQLAlchemy()

current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, '..', 'config.ini')

config = ConfigParser()
config.read(config_file_path)

class Database_Config:
    SQLALCHEMY_DATABASE_URI = config.get('database', 'SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = config.getboolean('database', 'SQLALCHEMY_TRACK_MODIFICATIONS')
