from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    Username = StringField(validators=[DataRequired()], default=None)
    Password = PasswordField(validators=[DataRequired()], default=None)
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    Username = StringField('Username', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', 'Passwords must match')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up ')


class FollowForm(FlaskForm):
    submit = SubmitField('Follow')


class UnfollowForm(FlaskForm):
    submit = SubmitField('Unfollow')


class CreatePostForm(FlaskForm):
    style = {'style': 'height: 100px'}
    name = StringField('Name', validators=[DataRequired()])
    caption = StringField('Caption', validators=[DataRequired()], render_kw=style)
    picture = FileField('Image', validators=[FileRequired(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Post')


class SearchForm(FlaskForm):
    name = StringField('Search ')
    submit = SubmitField('Search')


class UpdateForm(FlaskForm):
    Username = StringField('Username: ', render_kw={'readonly':True})
    image=FileField('Image:',validators=[FileRequired(['jpg','png','jpeg'])])
    submit = SubmitField('Update')
