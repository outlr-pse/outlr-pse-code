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

jwt_secret: str = os.getenv("JWT_SECRET_KEY") or config.get('jwt', 'secret_key')
db_url: str = os.getenv("DATABASE_URL") or config.get('database', 'url')
