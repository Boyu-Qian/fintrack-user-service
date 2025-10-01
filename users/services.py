import jwt
from datetime import datetime, timedelta
from config import Config
from users.models import User
from db import db

def create_user(email, password):
    if User.query.filter_by(email=email).first():
        raise ValueError(f"Email address:'{email}' already exists'")
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_email(email):
    return User.query.filter_by(email=email).first();

def get_user_by_id(user_id):
    return User.query.get(user_id);


def update_user(user, email=None, password=None):
    if email:
        user.email = email
    if password:
        user.set_password(password)
    db.session.commit()
    return user

def delete_user(user):
    db.session.delete(user)
    db.session.commit()

def get_all_users_count():
    return User.query.count()

def get_all_users():
    return User.query.all()

def authenticate_user(email, password):
    """
    Authenticate a user
    :param password:
    :return: JWT token if authenticated, else return None
    """
    user = User.query.filter_by(email=email).first()

    if not user:
        return None

    if not user.check_password(password):
        return None

    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }

    token = jwt.encode(payload, Config.PRIVATE_KEY, algorithm="RS256")
    return user,token

