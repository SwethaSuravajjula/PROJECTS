import os
from datetime import datetime
from dateutil.tz import tzlocal
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from forms import LoginForm, SignUpForm, CreatePostForm, FollowForm, UnfollowForm, SearchForm, UpdateForm

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/post_pics/'
app.config['UPLOAD_FOLDER1'] = 'static/profile_pics/'
db = SQLAlchemy(app)
Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):    #this is to ensure the multiuser nature of the application.
    return User.query.get(user_id)

#creating a many-to-many relationship table filling up both with user_id as a foreign key from User
followers = db.Table('followers', db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('users.id')))

#User Model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    post = db.relationship('Post', backref='author', cascade="all, delete-orphan", lazy=True)
    followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    profile_pic = db.Column(db.String(20),default='default.jpg')
    def __init__(self, username, password,profile_pic):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.profile_pic=profile_pic
    def remove(self):
        db.session.delete(self)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.get_id()).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def __repr__(self):
        f'{self.username}'

#Post Model
class Post(db.Model, UserMixin):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)
    pic = db.Column(db.String(20), nullable=False, default='default.jpg')

    def local_timestamp(self):
        return self.timestamp.astimezone(tzlocal())

    def __init__(self, title, text, user_id, pic):
        self.title = title
        self.text = text
        self.user_id = user_id
        self.pic = pic

    def __repr__(self):
        return f' {self.title}---{self.text}'


@app.route('/')
def home(): #Starting page of the website that redirects to the login page
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():   #defines the functionality of the login page should work
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.Username.data).first()
        if user is not None and user.check_password(form.Password.data):
            login_user(user)

            next = request.args.get('next')  #when user is searching for a website that requires login credentials thes pages would be appended
                                                #so that after logging they can hop on to the page that they are trying to access.

            if next is None or not next[0] == '/':
                next = url_for('general_feed')   # if there is non they would be redirected to the general feed
            return redirect(next)
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

# defines the functionality of signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    userall = User.query.all()
    if form.validate_on_submit():
        username = form.Username.data
        password = form.Password.data
        for users in userall:
            if username == users.username:
                return redirect(url_for('signup'))
        users = User(username, password,profile_pic=None)
        db.session.add(users)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

# defines the functionality of logout
@app.route('/logout')
@login_required
def logout():
    logout_user()   # this functionality is given by the flask login library
    return redirect(url_for("login"))

# provides the functionality in order to give a display the posts of the people the current user follows
@app.route('/General', methods=['GET', 'POST'])
@login_required
def general_feed():
    users = Post.query.order_by(Post.timestamp.desc())
    userall = User.query.all()
    return render_template('general_feed.html', users=users, userall=userall)

# this is a function in order to save the image that is posted
def save_image(picture_file):
    picture_filename = picture_file.filename
    picture_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], secure_filename(picture_filename))
    picture_file.save(picture_path)
    return picture_filename

# this is a function that describes the functionality of the creating a post
@app.route('/post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        name = form.name.data
        text = form.caption.data
        if form.picture.data:
            pics = save_image(form.picture.data)
            post = Post(name, text, current_user.id, pics)
            db.session.add(post)
            db.session.commit()
        return redirect(url_for('general_feed'))
    return render_template('create_post.html', form=form, user=current_user.username, title='Create')

#this describes the functionality of  showing the list of people following the current user
@app.route('/following/<username>', methods=['GET', 'POST'])
@login_required
def following(username):
    user = User.query.filter_by(username=username).first()
    lister = user.followed.all()
    form1 = FollowForm()
    form2 = UnfollowForm()
    return render_template('following.html', lister=lister, user=user.username, com_user=current_user.username,
                           form1=form1, form2=form2)

#this describes the functionality of  showing the  list of people the current user follows
@app.route('/follower/<username>', methods=['GET', 'POST'])
@login_required
def follower(username):
    user = User.query.filter_by(username=username).first()
    lister = user.followers.all()
    form1 = FollowForm()
    form2 = UnfollowForm()
    return render_template('followers.html', lister=lister, user=user.username, com_user=current_user.username,
                           form1=form1, form2=form2)

#this is the functionality of the button 'follow', which upon clicking the button appends the user's username into the desired person's
# followers list and the user's following list at the same time.
@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            return redirect(url_for('general_feed'))
        if user == current_user:
            return redirect(url_for('usernames', username=current_user.username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(request.referrer)
    else:
        return redirect(url_for('general_feed'))

#this is the functionality of the button 'unfollow', which upon clicking the button removes the user's username into the desired person's
# followers list and the user's following list at the same time.
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = UnfollowForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('general_feed'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('usernames', username=current_user.username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(request.referrer)
    else:
        return redirect(url_for('general_feed'))

# this function provides the functionality to display the user profile which also includes the current user profile also
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def usernames(username):
    user = User.query.filter_by(username=username).first()
    form1 = FollowForm()
    form2 = UnfollowForm()
    post = Post.query.filter_by(user_id=user.id).all()
    post_count = Post.query.filter_by(user_id=user.id).count()
    return render_template('Username.html', user=user, form1=form1, form2=form2, user_follow=user.followers.count(),
                           post=post, post_count=post_count)

# this function describes the functionality to delete the post created by the current_user
@app.route("/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
    return redirect(request.referrer)

# this function describes the functionality to update the post created by the current user
@app.route("/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    blog_post = Post.query.get_or_404(post_id)
    name = blog_post.title
    caption = blog_post.text
    picture = blog_post.pic
    if blog_post.author == current_user:
        form = CreatePostForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                blog_post.title = form.name.data
                blog_post.text = form.caption.data
                blog_post.pic = save_image(form.picture.data)
                db.session.commit()
                return redirect(url_for('general_feed'))
            elif request.method == 'GET':
                form.name.data = blog_post.title
                form.caption.data = blog_post.text
                form.picture.data = blog_post.pic
    return render_template('update_post.html', form=form, title='Update', name=name, caption=caption,picture=picture,
                           blog_post=blog_post)

# this function describes the functionality of searching the users to follow
@app.route('/Search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    form1 = FollowForm()
    form2 = UnfollowForm()
    users = db.session.query(User).filter(User.username != current_user.username)
    lister = []
    if form.validate_on_submit():
        name = form.name.data
        for u in users:
            if name in u.username:
                lister.append(u)
        return render_template('Search1.html', lister=lister, form=form, users=users, form1=form1, form2=form2)
    return render_template('Search.html', users=users, form=form, form1=form1, form2=form2)

# this function provides the functionality to delete the account of the current user
@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    current_user.remove()
    db.session.commit()
    return redirect(url_for('login'))
# this function provides the functionality to save the profile pic image of the user
def save_profile(picture_file):
    picture_filename = picture_file.filename
    picture_path = os.path.join(basedir, app.config['UPLOAD_FOLDER1'], secure_filename(picture_filename))
    picture_file.save(picture_path)
    return picture_filename
# this function provides the functionality to update the account of the user mostly to update the profile pic
@app.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    user = User.query.filter_by(username=current_user.username).first()
    name = user.username
    form = UpdateForm()
    if form.validate_on_submit():
        if form.image.data:
            profile=save_profile(form.image.data)
            user.profile_pic=profile
            db.session.commit()
            return redirect(url_for('general_feed'))
    return render_template('update_account.html', form=form, name=name)