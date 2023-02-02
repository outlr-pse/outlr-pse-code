from api.api import app
import database.database_access as db

db.setup_db()

if __name__ == '__main__':
    # Starts the api in debug mode for development. Do not use in production.
    app.run(host='localhost', port=5000, debug=True)
