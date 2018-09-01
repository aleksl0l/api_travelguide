from sqlalchemy import Column, Integer, String, Sequence

from app.app import db


class Roles(db.Model):
    __tablename__ = 'role'

    id_role_seq = Sequence('role_id_role_seq', metadata=db.metadata)

    id_role = Column(Integer,
                     server_default=id_role_seq.next_value(),
                     primary_key=True)
    name = Column(String(10))
