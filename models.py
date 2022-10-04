"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()

default_image = "https://socialnewsdaily.com/wp-content/uploads/2014/05/rick-astley-rickrolling.jpg"


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    image_url = db.Column(db.String(), default = default_image)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<{self.first_name} {self.last_name}>"

class Post(db.Model):
    '''Posts'''
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                     nullable=False)
    content = db.Column(db.String(350),
                     nullable=False)
    created_at = db.Column(DateTime, 
                     default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<{self.title} {self.content} {self.user_id}>"

class Tag(db.Model):

    __tablename__= 'tags'

    id = db.Column(db.Integer,
               primary_key=True,
               autoincrement=True)
    name = db.Column(db.String(50),
                    nullable=False,
                    unique = True)
    
    posts = db.relationship('Post', secondary = 'posts_tags' ,backref = 'tags')

class PostTag(db.Model):

    __tablename__ = 'posts_tags'

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
