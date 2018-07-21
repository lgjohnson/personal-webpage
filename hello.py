# Library Imports ---------------------------------------------------
import os

from dotenv import load_dotenv

from flask import Flask
from flask import request, redirect, abort, make_response
from flask import render_template, url_for, session, flash

from flask_moment import Moment
from flask_mail import Mail, Message

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

from datetime import datetime


# Instantiate App ---------------------------------------------------

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))


#read .env file to environment variables
load_dotenv()

#set Admin email
app.config['HOMEPAGE_ADMIN'] = os.getenv("HOMEPAGE_ADMIN")

#WTF configuration
app.config['SECRET_KEY'] = os.getenv("WTF_KEY")

#Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_SUBJECT_PREFIX'] = '[Flask Homepage]'
app.config['MAIL_SENDER'] = 'Homepage Admin <greg.flask.homepage@gmail.com>'

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#instantiate extensions
moment = Moment(app)
mail = Mail(app)
db = SQLAlchemy(app)

# Test Data ----------------------------------------------------------

blog_entries = [
	{'date': '6/1/2018', 'text': 'I fucked with Docker a bit.'},
	{'date': '5/20/2018', 'text': 'I did nothing.'},
	{'date': '5/05/2018', 'text': 'Read <em>Flask</em> by Michael Grinberg.'}
]

# Routes and Views ---------------------------------------------------

# HomePage

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
	return render_template('index.html', current_time = datetime.utcnow(), greetings=['hi there', 'how are you'])


# Portfolio

@app.route("/portfolio")
def portfolio():
	return redirect(url_for("indev"))

# Blog
@app.route("/blog")
def blog():
	return render_template('blog.html', blog_entries=blog_entries)

# Contact Me

@app.route("/contactme", methods=['GET', 'POST'])
def contactme():
	form_data = None
	form = ContactForm(request.form)
	if form.validate_on_submit():
		form_data = {
			'Name': form.name.data,
			'Company': form.company.data,
			'Position': form.position.data,
			'Email': form.email.data,
			'Content': form.content.data
		}
		form.name.data = ''
		form.company.data = ''
		form.position.data = ''
		form.email.data = ''
		form.content.data = ''
		session['form_data'] = form_data
		flash('Thanks for reaching out ' + form_data['Name'] + '!')
		if app.config['HOMEPAGE_ADMIN']:
			send_email(
				app.config['HOMEPAGE_ADMIN'],
				app.config['HOMEPAGE_ADMIN'],
				'New Message',
				'From {}, a {} at {}: \n{}\nFrom {}'.format(
					form_data['Name'],
					form_data['Position'],
					form_data['Company'],
					form_data['Content'],
					form_data['Email']
				)
			)
		return redirect(url_for('contactme'))
	return render_template('contactme.html', form=form, form_data = session.get('form_data'))


# Under Development
@app.route("/indev")
def indev():
	return render_template('indev.html')

#404 error handler
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

#500 error handler
@app.errorhandler(500)
def internal_server_error():
	return render_template('500.html'), 500




#Test Pages

@app.route("/greet<name>")
def greet(name):
	return render_template('name.html', name=name)

@app.route("/test")
def testMe():
	return '<p>The HTTP request method was {} and it is {} that it is secure.</p>'.format(
		request.method, str(request.is_secure))


# Forms ---------------------------------------------------

class ContactForm(FlaskForm):
	name = StringField('Name:', validators=[DataRequired()])
	company = StringField('Company:', validators=[DataRequired()])
	position = StringField('Position:', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	content = TextAreaField('Message', validators=[DataRequired()])
	submit = SubmitField('Send')

# Email Function ------------------------------------------

def send_email(to, sender, subject, body):
	msg = Message(
		app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
		sender=sender, recipients=[to])
	msg.body = body
	#msg.html = render_template(template + '.html', **kwargs)
	mail.send(msg)


# Database Models ------------------------------------------

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref = 'role')

	def __repr__(self):
		return '<Role {}>'.format(self.name)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

