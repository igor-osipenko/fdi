from wtforms import TextField, PasswordField, validators, SelectField, TextAreaField, BooleanField, HiddenField
from flask_wtf import Form
from models import Subject, OS

SECRET_KEY = 'Z]\x17\x0f\xb6\xd4\x8c7\x85\xa6s7\x9e\xba?\xe0\xeb\x02\xb4P\x04R\xe6>'


class RegistrationForm(Form):
    name = TextField('Name', [validators.Length(min=3, max=25)])
    email = TextField('Email', [
        validators.Length(min=6, max=35),
        validators.Email()
    ])

    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

    confirm = PasswordField('Confirm Password')

class LoginForm(Form):
    email = TextField('Email', [
        validators.Required(),
        validators.Length(min=6, max=35),
        validators.Email()
    ])
    password = PasswordField('Password', [validators.Required()])


class AdminLoginForm(Form):
    email = TextField('Email', [
        validators.Required(),
        validators.Length(min=6, max=35),
        validators.Email()
    ])
    password = PasswordField('Password', [validators.Required()])


class OrderForm(Form):
    title = TextField('Order title', [validators.Length(min=3, max=30)])
    subject = SelectField('Subject', choices=[], coerce=int, validators=[validators.Required()], id='subject')
    category = SelectField('Category', choices=[], id="categories", coerce=int, validators=[validators.Required()])
    os = SelectField('OS', choices=[], id="os", coerce=int, validators=[validators.Required()])
    deadline = TextField('Deadline', [validators.DataRequired()])
    details = TextAreaField('Details', [validators.DataRequired()])
    explanations = BooleanField('I need detailed explanations', id='explanations')

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        Form.__init__(self, formdata, obj, prefix, **kwargs)
        self.subject.choices=[(s.id, s.name) for s in Subject.query]
        self.os.choices=[(o.id, o.name) for o in OS.query]