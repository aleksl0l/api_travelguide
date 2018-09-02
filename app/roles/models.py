from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# from app.app import db
Base = declarative_base()


class Roles(Base):
    __tablename__ = 'role'

    # id_role_seq = Sequence('role_id_role_seq', metadata=Base.metadata)

    id_role = Column(Integer,
                     # server_default=id_role_seq.next_value(),
                     primary_key=True)
    name = Column(String(10))
