"""SQLAlchemy models for blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance
db = SQLAlchemy()

# Default profile image if user doesn't provide one
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User(db.Model):
    """Site user."""

    __tablename__ = "users"  # Specify the table name in the database

    # Primary key for user identification
    id = db.Column(db.Integer, primary_key=True)
    # User's personal information
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    # Relationship to Post model - allows cascade deletion of related posts
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""
        # Combine first and last name for display
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Blog post."""

    __tablename__ = "posts"  # Specify the table name in the database

    # Post attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    # Automatically set creation timestamp
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    # Foreign key to link post to its author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""
        # Format: "Mon Jan 1 2024, 12:00 PM"
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


def connect_db(app):
    """Connect this database to provided Flask app."""
    # Bind Flask app to SQLAlchemy instance
    db.app = app
    db.init_app(app)