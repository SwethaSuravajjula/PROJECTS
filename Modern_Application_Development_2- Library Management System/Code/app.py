from flask import Flask, request, render_template, jsonify, make_response, send_file,Response
from models import *  # connecting database to the flask app
from flask_security import Security, SQLAlchemyUserDatastore, logout_user, roles_accepted, auth_required,hash_password,roles_required
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user, current_user
import secrets
from flask_cors import CORS
from functools import wraps
from datetime import datetime, timedelta
from flask_restful import Api
from datetime import datetime
import os 
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import func
from workers import celery_init_app
from tasks import *

import flask_excel as excel
from celery.result import AsyncResult
from celery.schedules import crontab
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from collections import Counter

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./library_db.sqlite3'
app.config['SECRET_KEY'] = 'cde3dc5fd9b4430d8db02a9a6f777a1d'
app.config['SECURITY_PASSWORD_SALT'] = secrets.token_bytes(16)  # 16 bytes (128 bits) salt
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
app.config['UPLOAD_FOLDER'] = 'static/documents/'
app.config['UPLOAD_FOLDER_IMAGE'] = 'static/images/'
app.config['UPLOAD_FOLDER_PROFILE'] = 'static/profiles/'
api=Api(app)
app.app_context().push()
db.init_app(app) 
excel.init_excel(app) #connecting database to the flask app
app.app_context().push() 
celery_app = celery_init_app(app)
CORS(app)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


def roles(): #creating roles for admin and user 
    roles_permissions = {
        'admin':'admin-access',
        'user':'user-access'
    }
    #Iterating over each role 
    for role_name,role_permissions in roles_permissions.items():
        role=Role.query.filter_by(name=role_name).first()
        if not role:
            user_datastore.find_or_create_role(name=role_name, description=role_permissions)
    db.session.commit()

def admin_user():
    if not user_datastore.find_user(email="admin@email.com"):
        user_datastore.create_user(username='Admin',email="admin@email.com", password=generate_password_hash("admin"), roles=['admin'])
        db.session.commit()
    return True

@app.route('/api/login',methods=['POST'])  # this is a login api
def login():
    if request.method=='POST':
        data = request.get_json()
        name=data.get('name')
        email = data.get('email')
        password=data.get('password')
        if not email:
            return jsonify({"message": "email not provided"}), 400

        user = user_datastore.find_user(email=email)

        if not user:
            return jsonify({"message": "User Not Found"}), 404

        if check_password_hash(user.password,password): # checking whether the password is correct or not
                token = user.get_auth_token()
                response=jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name})
                response.set_cookie('Authentication-Token', token)
                user_id = User.query.filter_by(username=name,email=email).first().id
                activity = UserActivity(user_id=user_id, activity_type='login')
                db.session.add(activity)
                db.session.commit()
                
                return response
        else:
            return jsonify({"message": "Wrong Password"}), 400
    
    
@app.route('/api/register',methods=['POST'])  # this is for user registration and there is no admin registration
def register():
    users=User.query.all()
    data = request.get_json()
    name=data['name']
    email = data['email']
    password = data['password']
    hashed_password = generate_password_hash(password)  # generates the hashed password 
    try:
        for user in users:
            if user.email==email or user.username==name:
                return make_response(jsonify({'message':'Email/username is already taken'}),400)
        general_user = user_datastore.create_user(username=name,email=email, password=hashed_password)
        user_datastore.add_role_to_user(general_user, 'user')
        db.session.commit()
        user_id = User.query.filter_by(username=name,email=email).first().id
        activity = UserActivity(user_id=user_id, activity_type='registered')
        db.session.add(activity)
        db.session.commit()
        return make_response(jsonify({'message': 'User has been registered successfully'}), 200)
    except:
        # Handle the case when the email already exists
        return make_response(jsonify({'message': 'This email is already registered. Please use a different email.'}), 400)  
    

@app.route('/api/sections', methods=['GET'])
@auth_required('token')
@roles_accepted('user', 'admin')
def get_sections():
    if request.method == 'GET':
        sections = Section.query.order_by(Section.date_created.desc()).all()
        sections_data = []
        for section in sections:  # Initializing the books_data list for each section
           
            books_data = []
            for book in section.books:  # Appending book ID to books_data list
               
                books_data.append((book.id,book.name))
            
            section_data = {   # Creating section data dictionary including book IDs
                'section_id': section.id,
                'section_name': section.name,
                'section_description': section.description,
            }
            sections_data.append(section_data)
            
        return jsonify({'sections': sections_data}), 200




@app.route('/api/sections/<int:section_id>/books', methods=['GET'])
@auth_required('token')
@roles_accepted('user', 'admin')
def get_books(section_id):
    if request.method == 'GET':
        section = Section.query.get(section_id)
        if not section:
            return jsonify({'message': 'Section not found'}), 404
        
        books = Book.query.filter_by(section_id=section_id).order_by(Book.date_created.desc()).all()

        books_data = []

        for book in books:

            book_data = {
                'id': book.id,
                'name': book.name,
                'book': book.content,
                'authors': book.authors,
                'book_image' : book.book_pic,
                'total_copies': book.total_copies,
                'available_copies': book.available_copies,
                'no_of_pages': book.no_of_pages,
            }
            books_data.append(book_data)

        return jsonify({'books': books_data}), 200


@app.route('/api/request-book/<int:book_id>', methods=['POST'])
@auth_required('token')
@roles_accepted('user')
def request_book(book_id):
    if request.method == 'POST':
        
        if not current_user.is_authenticated: # for authentication purposes 
            return make_response(jsonify({'message': 'User not authenticated'})), 401

        book = Book.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found'})), 404
                
        if len(current_user.issues) >= 5:# Checking if the user has already requested the maximum allowed number of books which is greater  or equal to 5
            return make_response(jsonify({'message': 'You have reached the maximum limit of requested books'})), 400
        
        current_issue = Issue.query.filter_by(user_id=current_user.id, book_id=book_id).first()
        if current_issue: # Checking if  the user is asking for a book that has already been issued 
            days_remaining = (current_issue.return_date - datetime.now()).days
            return make_response(jsonify({'message': f'This book has already been issued to you and is due in {days_remaining} days'})),400
        
        if book.available_copies > 0:
            book_issue = Issue(user_id=current_user.id, book_id=book_id, section_id=book.section_id)
            db.session.add(book_issue)
            book.available_copies = book.available_copies - 1 
            db.session.commit()
            activity = UserActivity(user_id=current_user.id, activity_type=f'issued book {book.name} from section {book.section.name}')#entering the log
            db.session.add(activity)
            db.session.commit()

            return make_response(jsonify({'message': 'Book issued successfully'})), 200
        else:
            return make_response(jsonify({'message': 'Book requested out of stock'})),400

@app.route('/api/user/cart', methods=['GET'])  # this is to create a user's cart 
@auth_required('token')
@roles_accepted('user')
def user_cart():
    if request.method == 'GET':
        issues=Issue.query.filter_by(user_id=current_user.id).all()
        user=User.query.get(current_user.id)
        issued=[]
        if issues:
            for issue in issues:
                temp={
                    'issue_id': issue.id,
                    'book' : issue.book.name,
                    'content':issue.book.content,
                    'authors' : issue.book.authors,
                    'image' : issue.book.book_pic,
                    'section_name' : issue.book.section.name,
                    'issue_date': issue.issue_date.isoformat(),
                    'return_date': issue.return_date.isoformat() if issue.return_date else None,
                    'section_id' : issue.section_id,
                    'book_id': issue.book_id,
                    'user_email' : user.email,
                    'user_username' : user.username

                    }
                issued.append(temp)
            return jsonify({'issued':issued}),200
        else:
            return make_response({'message':'No books issued'}),400
        
@app.route('/api/pdfissue/<int:book_id>',methods=['GET'])   # this is to fetch the pdf book embedded inside the vuejs application 
@auth_required('token')
@roles_required('user')      
def get_pdf(book_id):
    
        book = Book.query.get(book_id)
        if book:
            book_name=book.content
            return jsonify({'book_name':book_name}),200
        else:
            return jsonify({'message':'book not issued/found'}),400

           


@app.route('/api/return-book/<int:book_id>', methods=['POST'])
@auth_required('token')
@roles_accepted('user')
def return_book(book_id): # this api ensures safe returning of the book
    if request.method == 'POST':
        if not current_user.is_authenticated: #this is for the authentication purposes
            return make_response(jsonify({'message': 'User not authenticated'})), 401

        book = Book.query.get(book_id)
        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)
        
        
        issue = Issue.query.filter_by(user_id=current_user.id, book_id=book_id).first()# Checking if the user has borrowed the book
        if issue:
            book.available_copies = book.available_copies + 1  # incerementing the copy of the book so that others can now request for this book
            db.session.commit()
            db.session.delete(issue) # deleting the issue 
            db.session.commit()
            activity = UserActivity(user_id=current_user.id, activity_type=f'returned book {book.name} from section {book.section.name}')
            db.session.add(activity)
            db.session.commit()
            return make_response(jsonify({'message': 'Book returned successfully'}), 200)
        else:
            return make_response(jsonify({'message': 'You have not borrowed this book'}), 400)



@app.route('/api/admin/sections', methods=['POST'])
@auth_required('token')
@roles_required('admin')
def create_section(): 
    if request.method == 'POST': # this api creates a new section
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        existing_section = Section.query.filter_by(name=name, description=description).first() # Checkpoint whether the same name and description already exists
        if existing_section:
            return jsonify({'message': 'A section with the same name and description already exists'}), 400
        
        
        section = Section(name=name, description=description)# Creating and adding the new section if it doesn't already exist
        db.session.add(section)
        db.session.commit()
        
        return jsonify({'message': 'Section created successfully'}), 201


@app.route('/api/admin/sections/<int:section_id>', methods=['GET','PUT'])
@auth_required('token')
@roles_required('admin')
def update_section(section_id): # updating the section typically either the section name or the description of the section
    if request.method == 'GET': # this api fetches the section
        section=Section.query.get(section_id)
        sections={'name':section.name,'description':section.description}
        if not section:
            return jsonify({'message': 'Section not found'}), 404
        return jsonify({'section':sections}),200

    if request.method == 'PUT':  # this api updates the section
        section = Section.query.get(section_id)
        if not section:
            return jsonify({'message': 'Section not found'}), 404
        
        data = request.get_json()
        section.name = data.get('name', section.name)
        section.description = data.get('description', section.description)
        db.session.commit()
        
        return jsonify({'message': 'Section updated successfully'}), 200

@app.route('/api/admin/sections/<int:section_id>', methods=['DELETE'])
@auth_required('token')
@roles_required('admin')
def delete_section(section_id):
    if request.method == 'DELETE': # this api deletes the section
        section = Section.query.get(section_id)
        books = Book.query.filter_by(section_id=section_id).all()
        feedbacks=Feedback.query.filter_by(section_id=section_id).all()
        if not section:
            return jsonify({'message': 'Section not found'}), 404
        
       
        issues = Issue.query.filter_by(section_id=section_id).all()# Checking whether any active issues related to books in this section are present before deletion
        if issues:
            return jsonify({'message': 'Books in this section are in use'}), 400
        else:  
            db.session.delete(section) 
            for book in books:
                db.session.delete(book)
            for feedback in feedbacks:
                db.session.delete(feedback)
            db.session.commit()
            return jsonify({'message': 'Section deleted successfully'}), 200

def save_document(document_file): # this is a function to save the filename in the database and save the actual document in the local directory static/documents
    document_filename = document_file.filename.replace(' ', '_').replace(')', '').replace('(', '')
    document_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], secure_filename(document_filename))
    document_file.save(document_path)
    return document_filename
def save_pic(file):# this is a function to save the filename in the database and save the actual image in the local directory static/images
    document_filename = file.filename.replace(' ', '_').replace(')', '').replace('(', '')
    document_path = os.path.join(basedir, app.config['UPLOAD_FOLDER_IMAGE'], secure_filename(document_filename))
    file.save(document_path)
    return document_filename

@app.route('/api/admin/sections/<int:section_id>/books', methods=['POST'])
@auth_required('token')
@roles_required('admin')
def create_book(section_id):
    if request.method == 'POST': # this creates the book in a particular section
        section = Section.query.filter_by(id = section_id).first()
        if not section:
            return jsonify({'message': 'Section not found'}), 404
        
        #data = request.get_json()
        name = request.form['name']  # these all fetch data from the encapsulated form in the frontend
        book_pic=request.files['book_pic']
        content = request.files['content']
        authors = request.form['authors']
        no_of_pages= request.form['no_of_pages']
        if request.files.get('content'):
            content_name = save_document(request.files.get('content'))  # gets the uploaded file into local directory
        if request.files.get('book_pic'):
            pic_name= save_pic(request.files.get('book_pic'))
        
        if not name or not content or not authors or not book_pic:
            return make_response(jsonify({'message': 'Name, content, authors, and document are required fields'})), 400
        
        
        existing_book = Book.query.filter_by(name=name, section_id=section_id).first()  # Checking if a book with the same name already exists in the section
        if existing_book:
            return make_response(jsonify({'message': 'A book with the same name  or pic already exists in this section'})), 400      
        
        book = Book(name=name, content=content_name,book_pic=pic_name, authors=authors, section_id=section_id, no_of_pages=no_of_pages)   # finally creates a new book
        db.session.add(book)
        db.session.commit()
        
        return jsonify({'message': 'Book created successfully'}), 201
        

@app.route('/api/admin/sections/<int:section_id>/books/<int:book_id>', methods=['GET', 'PUT'])
@auth_required('token')
@roles_required('admin')
def update_book(section_id, book_id):
    if request.method == 'GET': 
        book = Book.query.filter_by(id=book_id, section_id=section_id).first() 
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        return jsonify({'book': book.search()}), 200

    if request.method == 'PUT': # this modifies a book in a particular section
        book = Book.query.filter_by(id=book_id, section_id=section_id).first()
        if not book:
            return make_response(jsonify({'message': 'Book not found in the section'})), 404

        
        if book.available_copies != book.total_copies: # Checking if the book is currently issued
            return make_response(jsonify({'message': 'Cannot update an issued book'})), 400

        
        name = request.form.get('name')  # data from the form
        authors = request.form.get('authors')
        no_of_pages = request.form.get('no_of_pages')

       
        if 'content' in request.files:  # Checking if content is included in the request
            content_file = request.files['content']
            if content_file:
                content_name = save_document(content_file)
                book.content = content_name     
        if name:               # Updating the  book details
            book.name = name
        if authors:
            book.authors = authors
        if no_of_pages:
            book.no_of_pages = no_of_pages

        db.session.commit()

        return make_response(jsonify({'message': 'Book updated successfully'})), 200
    
@app.route('/api/admin/sections/<int:section_id>/books/<int:book_id>', methods=['DELETE'])
@auth_required('token')
@roles_required('admin')
def delete_book(section_id, book_id):
    book = Book.query.filter_by(id=book_id, section_id=section_id).first()
    if not book:
        return make_response(jsonify({'message': 'Book not found in the section'})), 404

    
    if book.available_copies != book.total_copies:   # Checking if the book is currently issued
        return make_response(jsonify({'message': 'Cannot delete an issued book'})), 400

   
    db.session.delete(book)  # Deletes the book

    
    feedback = Feedback.query.filter_by(book_id=book_id,section_id=book.section_id).all() # Deleting the related feedback
    for fb in feedback:
        db.session.delete(fb)
        
    db.session.commit()


    

    return make_response(jsonify({'message': 'Book deleted successfully'})), 200

def book_is_issued(book):
    
    issues = Issue.query.filter_by(book_id=book.id, return_date=None).all() # Checking if the book is currently issued
    return len(issues) > 0

@app.route('/api/admin', methods=['GET'])
@auth_required('token')  
@roles_accepted('admin')  
def user_details():
    users = User.query.all()
    user_list = []
    if users:
        for user in users:
            if user.email != "admin@email.com":
                user_data = {
                    'id': user.id,
                    'email': user.email,
                    'active': user.active
                    
                }
                user_list.append(user_data)
        
        return jsonify(user_list), 200
        
    else:
        return jsonify({'message': 'No Users'}), 404


@app.route('/api/admin/<int:user_id>', methods=['GET'])
@auth_required('token')  
@roles_accepted('admin') 
def get_user_details(user_id): #this fetches the user details
    user = User.query.get(user_id)
    issues = Issue.query.filter_by(user_id=user_id).all()
    if user:
        issued_books = []
        if issues:
            for issue in issues:
                book = Book.query.get(issue.book_id)
                if book:
                    issued_books.append({
                    'issue_id': issue.id,
                    'issue_email': issue.user.email,
                    'book_issued':issue.book.name,
                    'section_of_the_book':issue.book.section.name,
                    'issue_date': issue.issue_date.isoformat(),
                    'return_date': issue.return_date.isoformat() if issue.return_date else None
                    
                   })
        user_data = {
            'id': user.id,
            'email': user.email,
            'active': user.active,
            'issue' : issued_books
            
        }
        

        return jsonify({'users': user_data}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/api/admin/activity', methods=['GET'])
@auth_required('token')  
@roles_accepted('admin')  
def get_user_activity():
    user_activity = UserActivity.query.all()
    if user_activity:
        activity_data = [activity.serialize() for activity in user_activity if activity.user_id != 1]
        return jsonify({'activity': activity_data}), 200
    else:
        return jsonify({'message': 'No activity found for this user'}), 404
    
@app.route('/api/feedback/<int:book_id>', methods=['GET','POST'])
@auth_required('token') 
@roles_required('user') 
def post_feedback(book_id):
    if request.method=='GET': # fetches all the feedbacks 
        feedbacks=Feedback.query(book_id=book_id).all()
        feedback=[]
        for feed in feedbacks:
            temp={
                'id':feed.id,
                'user' : feed.user.username,
                'book' : feed.book.name,
                'section' : feed.book.section.name,
                'rating' : feed.rating,
                'comment' : feed.comment

            }
            feedback.append(temp)
        return jsonify({'feedback':feedback}),200
    
    if request.method == 'POST': # allows submission of a feedback by a user 
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment')
        user_feedback=Feedback.query.filter_by(user_id=current_user.id,book_id=book_id).all()
        book=Book.query.get(book_id)
        if user_feedback:
            return make_response(jsonify({'message': 'You already gave a feedback to this book' })), 400
    
        if not (book_id and rating): # Checking if all required data is provided
            return make_response(jsonify({'message': 'Book ID and rating are required'})), 400

    
        new_feedback = Feedback(user_id=current_user.id, book_id=book_id, section_id=book.section_id, rating=rating, comment=comment)


        db.session.add(new_feedback)
        db.session.commit()

        return make_response(jsonify({'message': 'Feedback posted successfully'})), 201

    
@app.route('/api/user/feedback',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def feedback():
    if request.method=='GET': # getting all the feedback of the books 
        feedback=Feedback.query.all()
        feedbacks=[]
        for feed in feedback:
            temp={
                'id':feed.id,
                'user' : feed.user_id,
                'book' : feed.book_name,
                'section' : feed.section_name,
                'rating' : feed.rating,
                'comment' : feed.comment

            }

            feedbacks.append(temp)
        return jsonify({'feedback':feedbacks}),200
    else:
        return make_response(jsonify({'Method not allowed'})),400
    

    
@app.route('/api/admin/issue',methods=['GET'])
@auth_required('token')
@roles_required('admin')
def issued_books(): #getting all the issued books 
    issue=Issue.query.all()
    issued_books=[]
    for iss in issue:
        temp={
            'name':iss.user.username,
            'book':iss.book.name,
            'section':iss.book.section.name,
            'return_date': iss.return_date,
            'issue_date':iss.issue_date

        }
        issued_books.append(temp)

    return jsonify({'issue':issued_books}),200


@celery_app.on_after_configure.connect
def setup_daily_reminder(sender,**kwargs): # this is for daily remainder asking for an inactive user to login in for that day
    sender.add_periodic_task(
        crontab(minute=53, hour=8),
        daily_reminder.s()
    )
 
@celery_app.on_after_configure.connect # this is a for montly remainder giving the report for the user about what has happened and so on
def setup_monthly_reminder(sender,**kwargs):
    sender.add_periodic_task(
        crontab(minute=53, hour=8,day_of_month=17),
        monthly_reminder.s()
    )

@celery_app.on_after_configure.connect  # this automatically revokes the book from the user and sends an email to the user informing them that the access has been revoked
def setup_due_date_reminder(sender,**kwargs):
    sender.add_periodic_task(
        crontab(minute=53, hour=8),
        book_due_reminder.s()
    )




if  __name__ == '__main__':
    db.create_all()
    roles()
    admin_user()
    app.run(debug=True,port=7000)