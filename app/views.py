"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app, db, lm, oid
from flask import render_template, request, redirect, url_for,jsonify,g,session, flash

from flask.ext.wtf import Form 
from wtforms.fields import TextField # other fields include PasswordField 
from wtforms.validators import Required, Email
from app.models import MyProfile
from app.forms import LoginForm

from flask.ext.login import login_user, logout_user, current_user, login_required

class ProfileForm(Form):
     first_name = TextField('First Name', validators=[Required()])
     last_name = TextField('Last Name', validators=[Required()])
     # evil, don't do this
     image = TextField('Image', validators=[Required(), Email()])
     nickname = TextField('Nickname',validators=[Required()])
     email = TextField('Email',validators=[Required()])


@app.before_request
def before_request():
    g.user = current_user
    
@lm.user_loader
def load_user(id):
	return MyProfile.query.get(int(id))
	
###
# Routing for your application.
###
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        openid = request.form['openid']
        user = MyProfile.query.filter_by(nickname=openid).first()
        if user is None:
            return redirect(request.args.get('next') or url_for('index'))
        elif openid == user.nickname and user is not None:
            session['remember_me'] = form.remember_me.data
            oid.try_login(openid, ask_for=['nickname', 'email'])
            login_user(user)
            return redirect(url_for("index"))
 
    return render_template('login.html', title='Sign In',form=form, providers=app.config['OPENID_PROVIDERS'])
	
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = MyProfile.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = MyProfile(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
    
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template('home.html', title='Home', user=user, posts=posts)
                           
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile/', methods=['POST','GET'])
def profile_add():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        nickname = request.form['nickname']
        email = request.form['email']

        # write the information to the database
        newprofile = MyProfile(first_name=first_name, last_name=last_name, nickname=nickname, email=email)
        db.session.add(newprofile)
        db.session.commit()

        return "{} {} was added to the database of nickname {} ".format(request.form['first_name'],
                                             request.form['last_name'], request.form['nickname'])

    form = ProfileForm()
    return render_template('profile_add.html',
                           form=form)

@app.route('/profiles/',methods=["POST","GET"])
def profile_list():
    profiles = MyProfile.query.all()
    if request.method == "POST":
        return jsonify({"age":4, "name":"John"})
    return render_template('profile_list.html',
                            profiles=profiles)

@app.route('/profile/<int:id>')
def profile_view(id):
    profile = MyProfile.query.get(id)
    return render_template('profile_view.html',profile=profile)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
