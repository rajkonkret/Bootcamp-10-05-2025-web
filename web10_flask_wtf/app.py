from flask import Flask, render_template, url_for, request, flash, g, redirect, session
from flask_sqlalchemy import SQLAlchemy

import random
import string
import hashlib
import binascii

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin

app = Flask(__name__)

app.config.from_pyfile('config.cfg')


def get_hashed_password(password):
    os_urandom_static = b'\xee\x8b\x9c\xe6n\x96\xa9\xf5@\x99\x9c\xf3\xbf\xf1\x03\x86sr\x05\xcf\xa7\xac\xcf\xb2H\xfe\x7f\x10\x14\x9f%5\xde\xe5\xbd\xaef\x9d\xcd\xf4\xc9Be\xf9\x04\xf9\x1c}\xf9\x8a|\xe4\x92\xe1\xdb\xff~R\x0e\xb1'
    salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf=8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf=8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


if __name__ == '__main__':
    app.run(debug=True)
