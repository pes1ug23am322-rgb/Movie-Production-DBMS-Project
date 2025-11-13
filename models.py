from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, CheckConstraint

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(30))

class Production(db.Model):
    prod_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(50))
    language = db.Column(db.String(50))
    director = db.Column(db.String(100))

class Crew(db.Model):
    crew_id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('production.prod_id'))
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    production = db.relationship('Production', backref='crew')

class Casting(db.Model):
    cast_id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('production.prod_id'))
    actor_name = db.Column(db.String(100))
    character_name = db.Column(db.String(100))
    production = db.relationship('Production', backref='casting')

class Budget(db.Model):
    budget_id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('production.prod_id'), unique=True)
    estimated_cost = db.Column(db.Float)
    actual_cost = db.Column(db.Float)
    production = db.relationship('Production', backref='budget')

class Award(db.Model):
    award_id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('production.prod_id'))
    name = db.Column(db.String(200))
    category = db.Column(db.String(100))
    year = db.Column(db.Integer)
    production = db.relationship('Production', backref='awards')

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('production.prod_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    production = db.relationship('Production', backref='reviews')
    user = db.relationship('User', backref='reviews')

    __table_args__ = (
        CheckConstraint('rating BETWEEN 1 AND 10', name='valid_rating'),
    )
