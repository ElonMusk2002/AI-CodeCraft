# models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey, Table, Column, Integer, String
from sqlalchemy.orm import relationship
from app import db, login_manager

user_completed_challenges = Table(
    "user_completed_challenges",
    db.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("challenge_id", Integer, ForeignKey("coding_challenges.id")),
)


class UserProfile(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    skill_level = Column(Integer, default=1)
    preferred_languages = Column(String(200))
    preferred_topics = Column(String(200))

    completed_challenges = relationship(
        "CodingChallenge", secondary=user_completed_challenges, back_populates="users"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class CodingChallenge(db.Model):
    __tablename__ = "coding_challenges"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    difficulty = Column(Integer, nullable=False)
    programming_language = Column(String(50), nullable=False)
    topic = Column(String(50), nullable=False)

    users = relationship(
        "UserProfile",
        secondary=user_completed_challenges,
        back_populates="completed_challenges",
    )


@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))
