"""Blogly application."""
from collections import UserString
from crypt import methods
from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension
import unittest

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ihatechickens"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

default_image = "https://socialnewsdaily.com/wp-content/uploads/2014/05/rick-astley-rickrolling.jpg"

@app.route('/')
def home():
    return redirect ('/users')

@app.route('/users')
def user_list():
    '''Grabs the user table information from the database'''
    '''lists all users in the database as links to profile'''
    users = User.query.all()
    return render_template('list.html', users = users)

@app.route('/users/new')
def user_add_form():
    '''The form to add a new user'''
    return render_template('form.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    '''THIS adds the user to the database'''
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or default_image)
    db.session.add(new_user)
    db.session.commit()
    '''Brings back to the list page'''
    return redirect('/')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user= User.query.get_or_404(user_id)
    return render_template('profile.html', user = user)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    user= User.query.get_or_404(user_id)
    return render_template ('edit.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def user_edit(user_id):
    user= User.query.get_or_404(user_id)
    user.first_name = request.form['first_name'],
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url'] or default_image

    db.session.add(user)
    db.session.commit()
    '''Brings back to the list page'''
    return redirect('/')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user= User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

# PART 2 added functions and routes

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user= User.query.get_or_404(user_id)
    return render_template('newpost.html', user = user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
    user= User.query.get_or_404(user_id)
    new_post = Post(
        title = request.form['title'],
        content = request.form['content'],
        user= user)
        
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template ('post.html', post = post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template ('postedit.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title'],
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')
    
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')