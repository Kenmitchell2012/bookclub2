from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models.user import User

db = "book_club"
class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.favorited = []
        print("from book init",self.creator)

    # add book to favorites

    # get all books
    @classmethod
    def get_all_books(cls):
        query = """
                SELECT * FROM books
                JOIN users on books.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        print(results)
        books = []
        for row in results:
            this_book = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": ""
            }
            this_book.creator = User(user_data)
            books.append(this_book)
            print(this_book)
        return books
    
    # get book by id
    @classmethod
    def get_book_by_id(cls, id):
        query = "SELECT * FROM books WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        return cls(results[0])

    
    # get book by user id
    @classmethod
    def get_book_by_user_id(cls, user_id, creator_id):
        query = """
                SELECT books.*, users.first_name as user_name FROM books
                JOIN users on books.user_id = users.id
                WHERE user_id = %(user_id)s
                AND creator_id = %(creator_id)s;
                """
        
        results = connectToMySQL(db).query_db(query, {"user_id": user_id, "creator_id": creator_id})
        if len(results) == 0:
            return None
        
        row = results[0]
        this_book = cls({
            'id': row['id'],
            'title': row['title'],
            'description': row['description'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
        })
        this_book.creator = {
            'user_id': row['user_id'],
            'name': row['user_name'],
        }
        return this_book
    
    # validate the book
    @staticmethod
    def validate_book(form_data):
        is_valid = True
        if len(form_data['title']) ==0:
            flash("Title is required!", 'book')
            is_valid = False
        if len(form_data['description']) < 2:
            flash("Descrption must be at least 2 characters long!", 'book')
            is_valid = False
        return is_valid
    
        # save book
    @classmethod
    def save_book(cls, data):
    
        query = """
                INSERT INTO books (title, description, user_id)
                VALUES (%(title)s, %(description)s, %(user_id)s);
                """
        return connectToMySQL(db).query_db(query, data)
    
    # update book
    @classmethod
    def update_book(cls, book_id, data):
        query = """
                UPDATE books SET title = %(title)s, description = %(description)s WHERE id = %(id)s;
                """
        data['id'] = book_id
        results = connectToMySQL(db).query_db(query, data)
        return results

    
    # delete book
    @classmethod
    def delete_book(cls, book_id):
        query = """
                DELETE FROM books WHERE id = %(book_id)s;
                """
        return connectToMySQL(db).query_db(query, {"book_id": book_id})
    