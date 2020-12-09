# ----------------------------------------------------------------------
# This script is used for database tables.
# for example,
#   User is database table  to store credentials of users
#
# @author: Reena Deshmukh <cs16b029@iittp.ac.in>
# @date: 12/02/2020
#
#-----------------------------------------------------------------------

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))