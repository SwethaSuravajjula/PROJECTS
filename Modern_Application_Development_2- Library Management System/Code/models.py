from flask_sqlalchemy import *
from sqlalchemy.ext.mutable import MutableSet
from flask_security import UserMixin,RoleMixin
from datetime import datetime,timedelta

db = SQLAlchemy()


class Section(db.Model):  # this is section table 
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.String())

    books = db.relationship('Book', backref='section', lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def search(self): # this is the search function of the section table; used for easy rendering of section elements 
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created.isoformat(),
            'description': self.description,
            'book_ids' : [book.id for book in self.books]
        }

class Book(db.Model): # this is the books table 
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    book_pic=db.Column(db.String(255))
    content = db.Column(db.String(255))
    authors = db.Column(db.String(255))
    date_issued = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    total_copies = db.Column(db.Integer, nullable=False, default=2)  
    available_copies = db.Column(db.Integer, nullable=False, default=2) 
    no_of_pages = db.Column(db.Integer,nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now()) 

    def __init__(self, name, content, authors, section_id,no_of_pages,book_pic):  # initialisation of the books table 
        self.name = name
        self.content = content
        self.authors = authors
        self.section_id = section_id
        self.no_of_pages=no_of_pages
        self.book_pic=book_pic

    def search(self): # this is the search function of the books table; used for easy rendering of the book elements 
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'authors': self.authors,
            'date_issued': self.date_issued.isoformat() if self.date_issued else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'section_id': self.section_id,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies
        }

class Issue(db.Model):
    __tablename__ = 'issue'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    section_id = db.Column(db.Integer, nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.now())
    return_date = db.Column(db.DateTime)

    def __init__(self, user_id, book_id,section_id):
        self.user_id = user_id
        self.book_id = book_id
        self.issue_date = datetime.now()
        self.section_id = section_id
        self.return_date = self.issue_date + timedelta(minutes=1) # this is just for testing purpose; generally it is for 7 days 

        # Update the date_issued and return_date of the associated book
        book = Book.query.get(book_id)
        if book and book.available_copies > 0:  # Check if there are available copies
            book.date_issued = self.issue_date
            book.return_date = self.return_date        

    user = db.relationship('User', backref='issues', lazy=True)
    book = db.relationship('Book', backref='issues', lazy=True)



class Feedback(db.Model):  # this is the feedback table 
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self,user_id,book_id,section_id,rating,comment): # this is the constructor of the feedback table 
        self.user_id=user_id
        self.book_id=book_id
        self.section_id=section_id
        self.rating=rating
        self.comment=comment
    @property
    def book_name(self):   # this is a property to find out the name of the book issued to the user 
        book = Book.query.get(self.book_id)
        return book.name if book else None

    @property
    def section_name(self):  # this is a property to find out the section name of the book issued to the user 
        book = Book.query.get(self.book_id)
        return book.section.name if book and book.section else None
    
    

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String, unique=False)  
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))
    
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)  #name of the role
    description = db.Column(db.String(255))       #description of the role

class UserActivity(db.Model):
    __tablename__ = 'UserActivity'
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    activity_type = db.Column(db.String(50), nullable=False)  # Type of activity performed, e.g., "login", "visit", etc.
    activity_timestamp = db.Column(db.DateTime, default=datetime.now()) 
    
    user = db.relationship('User', backref='activities', lazy=True) 

    def serialize(self):
        return{
            "id":self.id,
            "user_id":self.user_id,
            "user":self.user.username,
            "activity_type":self.activity_type,
            "activity_timestamp":self.activity_timestamp
        }