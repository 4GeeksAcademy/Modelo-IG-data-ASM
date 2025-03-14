from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    followers = relationship(
        "Follower", foreign_keys="[Follower.user_to_id]", back_populates="following")
    following = relationship(
        "Follower", foreign_keys="[Follower.user_from_id]", back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            # do not serialize the password, its a security breach
        }


class Follower (db.Model):
    __tablename__ = "follower"
    user_from_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id"), primary_key=True)

    follower = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    following = relationship("User", foreign_keys=[user_to_id], back_populates="followers")

    def serialize(self):
        return {
            "follower_id": self.user_from_id,
            "following_id": self.user_to_id, }


class Post (db.Model):
    __tablename__: "post"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    media = relationship("Media", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }


class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    comment_text: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(db.ForeignKey("Post.id"))

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }


class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    post_id: Mapped[int] = mapped_column(db.ForeignKey("post.id"))

    post = relationship("Post", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id,
        }