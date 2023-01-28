from api.api import app


def setup_db() -> None:
    """Sets up the database and collects all odms."""
    # TODO: Implement setup_db
    pass


setup_db()

if __name__ == '__main__':
    # Starts the api in debug mode for development. Do not use in production.
    app.run(host='localhost', port=5000, debug=True)
