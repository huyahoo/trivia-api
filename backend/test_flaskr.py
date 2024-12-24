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

            # Add sample questions
            question1 = Question(question="What is the capital of France?", answer="Paris", difficulty=1, category="1")
            question2 = Question(question="Who painted the Mona Lisa?", answer="Leonardo da Vinci", difficulty=2, category="2")
            db.session.add_all([question1, question2])
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

    def test_get_questions_success(self):
        """Test successful retrieval of paginated questions"""
        res = self.client.get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['total_questions'], 2)

    def test_get_questions_failure(self):
        """Test failure case for retrieving questions from an empty page"""
        res = self.client.get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_question_success(self):
        """Test successful deletion of a question"""
        with self.app.app_context():
            question = Question.query.first()

        res = self.client.delete(f'/questions/{question.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question.id)

    def test_delete_question_failure(self):
        """Test failure case for deleting a non-existing question"""
        res = self.client.delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    def test_add_question_success(self):
        """Test successful addition of a new question"""
        new_question = {
            "question": "What is the tallest mountain in the world?",
            "answer": "Mount Everest",
            "difficulty": 2,
            "category": "1"
        }

        res = self.client.post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_add_question_failure(self):
        """Test failure case for adding a question with missing fields"""
        incomplete_question = {
            "question": "What is the tallest mountain in the world?",
            "answer": "Mount Everest"
        }

        res = self.client.post('/questions', json=incomplete_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_search_questions_success(self):
        """Test successful search for questions"""
        search_data = {"searchTerm": "capital"}
        res = self.client.post('/questions/search', json=search_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))

    def test_search_questions_failure(self):
        """Test failure case for searching a question with no match"""
        search_data = {"searchTerm": "xyz123"}
        res = self.client.post('/questions/search', json=search_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)

    def test_get_questions_by_category_success(self):
        """Test successful retrieval of questions by category"""
        res = self.client.get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'], 1)

    def test_get_questions_by_category_failure(self):
        """Test failure case for questions in a non-existing category"""
        res = self.client.get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    def test_play_quiz_success(self):
        """Test successful quiz retrieval"""
        quiz_data = {
            "previous_questions": [],
            "quiz_category": {"type": "Science", "id": "1"}
        }

        res = self.client.post('/quizzes', json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn("question", data)

    def test_play_quiz_failure(self):
        """Test failure case for quiz with no questions in category"""
        quiz_data = {
            "previous_questions": [],
            "quiz_category": {"type": "Non-Existing", "id": "1000"}
        }

        res = self.client.post('/quizzes', json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNone(data['question'])

if __name__ == "__main__":
    unittest.main()
