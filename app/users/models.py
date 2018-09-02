from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# from app.app import db
from app.roles.models import Roles

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id_user = Column(Integer,
                     primary_key=True)
    public_id = Column(String(36))
    name = Column(String(50), unique=True)
    password = Column(String(100))
    id_role = Column(Integer, ForeignKey(Roles.id_role))
    # id_role_rel = relationship('Roles', foreign_keys=[id_role])
