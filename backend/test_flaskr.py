import unittest
import json
from flaskr import create_app
from models import setup_db, db, Category, Question
from settings import DB_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}_test",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            setup_db(self.app)
            db.create_all()
            # Add sample categories
            category1 = Category(type="Science")
            category2 = Category(type="Art")
            db.session.add_all([category1, category2])
            db.session.commit()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_categories_success(self):
        """Test successful retrieval of categories"""
        res = self.client.get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn("categories", data)
        self.assertEqual(len(data["categories"]), 2)

    def test_get_categories_failure(self):
        """Test failure case for retrieving categories when none exist"""
        with self.app.app_context():
            db.session.query(Category).delete()
            db.session.commit()

        res = self.client.get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')


if __name__ == "__main__":
    unittest.main()
