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

def is_localhost():
    """Check if the Flask application is running on localhost."""
    host = socket.gethostname()
    return host in ['localhost', '127.0.0.1', '::1']

def is_conda_environment():
    return "CONDA_DEFAULT_ENV" in os.environ

def is_docker_environment():
    return "DOCKER_CONTAINER" in os.environ

def is_ec2_environment():
    return "EC2" in os.environ

def is_ec2_for_selenium_environment():
    return "EC2_TEST" in os.environ

def is_github_actions():
    """Check if the code is running within a GitHub Actions pipeline."""
    return os.environ.get('GITHUB_ACTIONS') == 'true'

class Database_Config:
    if is_ec2_environment():
        if is_pytest_running():
            SQLALCHEMY_DATABASE_URI1 = config.get('database', 'SQLALCHEMY_DATABASE_URI1_AWS_TEST')
        else: 
            SQLALCHEMY_DATABASE_URI1 = config.get('database', 'SQLALCHEMY_DATABASE_URI1_AWS')
    elif is_ec2_for_selenium_environment():
        SQLALCHEMY_DATABASE_URI1 = config.get('database', 'SQLALCHEMY_DATABASE_URI1_AWS_TEST')
    else:
        if is_github_actions():
            SQLALCHEMY_DATABASE_URI1 = config.get('database', 'SQLALCHEMY_DATABASE_URI1_AWS_TEST')
        elif is_docker_environment():
            SQLALCHEMY_DATABASE_URI1 = config.get('database', 'SQLALCHEMY_DATABASE_URI1_DOCKER')
        else: 
            SQLALCHEMY_DATABASE_URI1 = config.get('database', 'SQLALCHEMY_DATABASE_URI1')

    SQLALCHEMY_TRACK_MODIFICATIONS = config.getboolean('database', 'SQLALCHEMY_TRACK_MODIFICATIONS')
