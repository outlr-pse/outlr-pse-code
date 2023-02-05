""" Configuration file for the application.

Reads the configuration from the config.ini file or from environment variables.
The environment variables take precedence over the config.ini file.

Config variables are read from the following locations:
    - JWT secret key
        Environment variable: JWT_SECRET_KEY
        Config file [section] key: [jwt] secret_key
    - Database URL
        Environment variable: DATABASE_URL
        Config file [section] key: [database] url
"""

import configparser
import os

config = configparser.ConfigParser()
config.read('../config.ini')
#os.getenv("JWT_SECRET_KEY") or config.get('jwt', 'secret_key')
jwt_secret: str = "SECRET-KEY"
#os.getenv("DATABASE_URL") or config.get('database', 'url')
db_url: str = "postgresql://postgres:12345678@localhost:5432/outlr"
