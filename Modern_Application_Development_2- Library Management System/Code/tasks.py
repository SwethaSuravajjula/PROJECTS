from celery import shared_task
from models import *
from mailservice import send_email
from flask import Flask,render_template
from sqlalchemy import func
from flask_login import current_user


@shared_task(ignore_result=False)
def daily_reminder(): # this is for the daily reminder to alert the person to login if they have not done any login for that day.
    users = User.query.filter(User.id != 1).all()

    new_books_created = Book.query.filter(func.extract('day', Book.date_created) == datetime.now().day).all()  
    
    for user in users: 
        user_login_today = UserActivity.query.filter(
            UserActivity.user_id == user.id,
            func.extract('day', UserActivity.activity_timestamp) == datetime.now().day,
            UserActivity.activity_type == 'login',
            
        ).all()
        
        if not user_login_today:
            no_booking_template = render_template('alert_login.html', name=user.username, new_books_created=new_books_created)
            send_email(user.email, "You are missing new updates !!!", no_booking_template)
    
@shared_task(ignore_result=False)
def monthly_reminder(): # this is for send out monthly report to all the users 
    
    users = User.query.all()

    for user in users:
        if user.username != 'Admin':
             issued_books = Issue.query.filter_by(user_id=user.id).all()
             books = Book.query.all()
        
             feedbacks = Feedback.query.all()

             activity_report = {
            'issued_books': [{'name': issue.book.name, 'user': issue.user.username, 'issue_date': issue.issue_date,'return_date': issue.return_date} for issue in issued_books],
            'ratings': [{'book_name': feedback.book_name,'section_name':feedback.section_name, 'rating': feedback.rating, 'comment': feedback.comment} for feedback in feedbacks]
            }

        
             template = render_template('monthly_report.html', name=user.username, activity_report=activity_report)
             send_email(user.email, "Monthly Report!!!", template)


@shared_task(ignore_result=False)
def book_due_reminder(): # this is to inform the users that they have exceeded the due date of the book issued and their acces has been revoked 
    users = User.query.all()

    for user in users:
        if user.username != 'Admin':
            issued_books = Issue.query.filter_by(user_id=user.id).all()
            due_daters = Issue.query.filter(Issue.return_date <= datetime.now(),Issue.user_id==user.id).all()
            books = []
            if due_daters:
                for issue in issued_books:
                    book=Book.query.get(issue.book_id)
                    if issue.return_date <= datetime.now():
                         temp = {
                            'issue_name': issue.book.name,
                            'issue_section': issue.book.section.name
                         }
                         db.session.delete(issue)
                         book.available_copies = book.available_copies + 1
                         useractivity=UserActivity(user_id=user.id,activity_type=f'book {temp["issue_name"] } belonging to section {temp["issue_section"]} has been successfully revoked')
                         db.session.add(useractivity)
                         db.session.commit()
                         template = render_template('due_date.html', name=user.username, temp=temp, books=books)
                         send_email(user.email, f'You have reached your book {temp["issue_name"]}\'s access limit !!!', template)

    
            


            
            


        
             

            
             