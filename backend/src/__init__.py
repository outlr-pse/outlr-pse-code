import database.database_access as db
from api.api import app
from odmprovider.pyod_scraper import PyODScraper


def setup_db() -> None:
    """Inserts all available ODMs into the database."""
    odms = PyODScraper().get_odms()
    for odm in odms:
        db.add_odm(odm)


setup_db()

if __name__ == '__main__':
    # Starts the api in debug mode for development. Do not use in production.
    app.run(host='localhost', port=5000, debug=True)
