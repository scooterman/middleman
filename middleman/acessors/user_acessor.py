# -*- coding: utf-8 -*-
# author: victor

from middleman.database import db
from middleman.models.users import User

def user_by_email(email):
    return db.session.query(User).filter(User.email == email).first()