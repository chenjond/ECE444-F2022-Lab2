from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
  name = StringField('What is your name?', validators=[DataRequired()])
  email = StringField('What is your UofT Email address?', validators=[DataRequired()])
  submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  form_submitted = False
  valid_email = False
  if form.validate_on_submit():
    form_submitted = True
    old_name = session.get('name')
    old_email = session.get('email')

    if old_name is not None and old_name != form.name.data:
      flash('Looks like you have changed your name!')
    if old_email is not None and old_email != form.email.data:
      flash('Looks like you have changed your email!')

    if "utoronto" in form.email.data:
      valid_email = True
    else:
      valid_email = False
    
    session['name'] = form.name.data
    session['email'] = form.email.data
    return redirect(url_for('index'))
  return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), valid_email=valid_email, form_submitted=form_submitted)

@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name, current_time=datetime.utcnow())
