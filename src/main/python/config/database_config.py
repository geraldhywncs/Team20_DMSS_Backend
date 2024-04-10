from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
import os
import socket
import sys

db = SQLAlchemy()

current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, '..', 'config.ini')

config = ConfigParser()
config.read(config_file_path)

def is_pytest_running():
    """Check if pytest is running."""
    return any('pytest' in arg for arg in sys.argv)

class Database_Config:
    #SQLALCHEMY_DATABASE_URI1 = config.get('database', 'SQLALCHEMY_DATABASE_URI1')
    SQLALCHEMY_DATABASE_URI1 = config.get('database', 'SQLALCHEMY_DATABASE_URI1_AWS')
    # if is_pytest_running():
    #     #TODO Gerald to change this to test DB
    #     SQLALCHEMY_DATABASE_URI1 = config.get('database', 'SQLALCHEMY_DATABASE_URI1')
    #TODO Gerald to add for AWS
    # elif AWS:
    #     SQLALCHEMY_DATABASE_URI1 = config.get('database', 'SQLALCHEMY_DATABASE_URI1_AWS')

    SQLALCHEMY_TRACK_MODIFICATIONS = config.getboolean('database', 'SQLALCHEMY_TRACK_MODIFICATIONS')
