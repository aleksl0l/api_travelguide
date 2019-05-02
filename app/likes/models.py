from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from app.sights.models import Sights
from app.users.models import Users

Base = declarative_base()


class Likes(Base):
    __tablename__ = 'likes'

    id_like = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey(Users.id_user))
    id_sight = Column(Integer, ForeignKey(Sights.id_sight))
    value = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('id_user', 'id_sight', name='likes__uc_id_user_id_sight'),)
