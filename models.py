import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=None):
    if database_path:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    else:
        database_url = os.environ.get('DATABASE_URL')
        if database_url and database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://", "postgresql://", 1
            )
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)


'''
Person
Have title and release year
'''
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(db.Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(db.Integer)
    gender = Column(String)

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
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }

  
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(db.Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(String)

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
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }

