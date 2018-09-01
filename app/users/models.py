from sqlalchemy import Column, Integer, String, ForeignKey, Sequence

from app.app import db
# from sqlalchemy.orm import relationship


class Users(db.Model):
    __tablename__ = 'users'

    id_user_seq = Sequence('users_id_user_seq', metadata=db.metadata)

    id_user = Column(Integer,
                     server_default=id_user_seq.next_value(),
                     primary_key=True)
    public_id = Column(String(36))
    name = Column(String(50), unique=True)
    password = Column(String(100))
    id_role = Column(Integer, ForeignKey('role.id_role'))
    # id_role_rel = relationship('Roles', foreign_keys=[id_role])
