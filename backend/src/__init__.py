from api.api import app
from database.database_access import setup_db

setup_db()

if __name__ == '__main__':
    # Starts the api in debug mode for development. Do not use in production.
    app.run(host='localhost', port=1337, debug=True)
