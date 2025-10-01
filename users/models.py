import uuid
from flask_sqlalchemy import SQLAlchemy
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    """
        User model for storing user account information.

        Attributes:
            id (string): Unique UUID identifier, serves as the primary key.
            username (string): The user's username, must be unique and non-nullable.
            email (string): The user's email address, must be unique and non-nullable.
            password_hash (string): Stores the hashed password (if using password login).
            created_at (DateTime): The user's creation time, automatically generated.

        Relationships:
            oauth_accounts (relationship): Links to the OAuthAccount model for
                                           third-party logins.
    """
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        """Returns a readable representation for debugging."""
        return f'<User {self.id}>'

    def set_password(self, password):
        """Hashes the plain-text password and stores it securely."""
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        """Verifies a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, password)