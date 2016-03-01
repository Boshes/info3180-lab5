from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID, COMMON_PROVIDERS
import sys
import logging


app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.config['SECRET_KEY'] = "this is a super secure key"
app.config['OPENID_PROVIDERS'] = COMMON_PROVIDERS
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://cpszstmfjktcva:Lc6vcVRVH8KJz4itSa21w8_-RG@ec2-54-227-250-148.compute-1.amazonaws.com:5432/d78fr778jcg850"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lab5:lab5@localhost/lab5"
db = SQLAlchemy(app)
db.create_all()
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app,'/tmp')

from app import views,models