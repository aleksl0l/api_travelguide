from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

# from app.app import db
from app.sights.models import Sights
from app.users.models import Users

Base = declarative_base()


class Likes(Base):
    __tablename__ = 'likes'

    # id_like_seq = Sequence('likes_id_like_seq', metadata=Base.metadata)

    id_like = Column(Integer,
                     # server_default=id_like_seq.next_value(),
                     primary_key=True)
    id_user = Column(Integer, ForeignKey(Users.id_user))
    id_sight = Column(Integer, ForeignKey(Sights.id_sight))
    value = Column(Integer, nullable=False)

    # id_user_rel = relationship('Users', foreign_keys=[id_user])
    # id_sights_rel = relationship('Sights', foreign_keys=[id_sight])
    __table_args__ = (UniqueConstraint('id_user', 'id_sight', name='likes__uc_id_user_id_sight'),)
