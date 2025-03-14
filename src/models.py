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

    Post = relationship("Post")
    Comment = relationship("Comment")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            # do not serialize the password, its a security breach
        }


class Post (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))

    user = relationship("user")
    comment = relationship("Comment")
    Media = relationship("Media")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    comment_text: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(db.ForeignKey("Post.id"))

    user = relationship("user")
    Post = relationship("Post")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.comment_text,
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    post_id: Mapped[int] = mapped_column(db.ForeignKey("Post.id"))

    Post = relationship("Post")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
        }
