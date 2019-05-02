from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Roles(Base):
    __tablename__ = 'role'

    id_role = Column(Integer, primary_key=True)
    name = Column(String(10))
