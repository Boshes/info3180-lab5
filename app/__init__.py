from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID, COMMON_PROVIDERS


app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a super secure key"
app.config['OPENID_PROVIDERS'] = COMMON_PROVIDERS

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lab5:lab5@localhost/lab5"
db = SQLAlchemy(app)
db.create_all()
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app,'/tmp')

from app import views
