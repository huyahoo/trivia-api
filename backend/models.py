from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from settings import DB_NAME, DB_USER, DB_PASSWORD

database_host = 'localhost:5432'
database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{database_host}/{DB_NAME}'

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    if not hasattr(app, 'db_initialized'):
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        app.db_initialized = True

class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    difficulty = Column(Integer, nullable=False)

    def __init__(self, question, answer, category_id, difficulty):
        self.question = question
        self.answer = answer
        self.category_id = category_id
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category_id,
            'difficulty': self.difficulty
        }

class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    questions = db.relationship('Question', cascade="all, delete-orphan", backref='category', lazy=True)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }