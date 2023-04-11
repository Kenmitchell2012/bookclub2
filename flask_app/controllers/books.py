from flask_app import app
from flask import render_template, redirect, url_for, request, flash, session
from flask_app.models.user import User
from flask_app.models.book import Book


@app.route('/createbook', methods=['POST'])
def create_book():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    print(session['user_id'])
    if not Book.validate_book(request.form):
        alert = 'Please fill all the fields'
        return redirect(url_for('dashboard', alert=alert))
    new_book = {
        'user_id': session['user_id'],
        'title': request.form['title'],
        'description': request.form['description']
    }
    print(new_book)
    Book.save_book(new_book)
    return redirect(url_for('dashboard'))