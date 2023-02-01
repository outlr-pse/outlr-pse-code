import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

jwt_secret: str = config.get('jwt', 'secret_key')
db_url: str = config.get('database', 'url')
