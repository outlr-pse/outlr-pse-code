from backend.src.api.mock_classes import MockDatabase
mock_database = MockDatabase()
from api.api import app
from database.database_access import setup_db

setup_db()

if __name__ == '__main__':
    # Starts the api in debug mode for development. Do not use in production.
    app.run(host='localhost', port=5000, debug=True)
