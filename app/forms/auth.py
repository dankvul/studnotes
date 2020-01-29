from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models.users import Group, User

style1 = {'class': 'form-control', 'id': 'inputUsername', 'placeholder': 'Enter username'}
style2 = {'class': 'form-control', 'id': 'inputPassword', 'placeholder': 'Enter password'}
style3 = {'class': 'form-control', 'id': 'inputCPassword', 'placeholder': 'Confirm password'}
style4 = {'class': 'form-check-input', 'id': 'remember-me-checkbox'}
style5 = {'class': 'form-control', 'id': 'inputToken', 'placeholder': 'Enter your group token'}


class AuthForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw=style1)
    password = PasswordField('Password', validators=[DataRequired()], render_kw=style2)
    remember_me = BooleanField('Remember me', render_kw=style4)
    submit = SubmitField('Login')


class NewGroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_name(self, name):
        group = Group.query.filter_by(name=name.data).first()
        if group is not None:
            raise ValidationError("Please use another name for group")


class RegForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw=style1)
    password = PasswordField('Password', validators=[DataRequired()], render_kw=style2)
    validating_password = PasswordField(
        'Confirm password', validators=[DataRequired(), EqualTo('password')], render_kw=style3)
    token = StringField('Enter token', validators=[DataRequired()], render_kw=style5)
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use another username")

    def validate_token(self, token):
        group = Group.query.filter_by(reg_token=token.data).first()
        if group is None:
            raise ValidationError("Wrong token")

