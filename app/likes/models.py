from sqlalchemy import Column, Integer, ForeignKey, Sequence, UniqueConstraint
from sqlalchemy.orm import relationship
from app.app import db


class Likes(db.Model):
    __tablename__ = 'likes'

    id_like_seq = Sequence('likes_id_like_seq', metadata=db.metadata)

    id_like = Column(Integer,
                     server_default=id_like_seq.next_value(),
                     primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id_user'))
    id_sight = Column(Integer, ForeignKey('sights.id_sights'))
    value = Column(Integer, nullable=False)

    id_user_rel = relationship('Users', foreign_keys=[id_user])
    id_sights_rel = relationship('Sights', foreign_keys=[id_sight])
    __table_args__ = (UniqueConstraint('id_user', 'id_sight'),)