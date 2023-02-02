import unittest
import database.database_access as db
from backend.src import setup_db
from database.database_access import Base


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.drop_all(bind=db.engine, checkfirst=True)
        Base.metadata.create_all(bind=db.engine)
        setup_db()

    # def test_scraper(self):
    #     odms = db.get_all_odms()
    #     odm_names = [odm.name for odm in odms]
    #     self.assertIn('cd.CD', odm_names)
    #     self.assertIn('hbos.HBOS', odm_names)
    #     self.assertIn('anogan.AnoGAN', odm_names)
    #     self.assertIn('abod.ABOD', odm_names)
    #     self.assertIn('alad.ALAD', odm_names)
    #     self.assertIn('rod.ROD', odm_names)
    #     self.assertIn('knn.KNN', odm_names)
