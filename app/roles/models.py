from sqlalchemy import Column, Integer, String, REAL, Text, ForeignKey, Sequence, ARRAY, UniqueConstraint
from sqlalchemy.orm import relationship
from app.app import db

class Roles(db.Model):
    __tablename__ = 'roles'

    id_role_seq = Sequence('roles_id_role_seq', metadata=db.metadata)

    id_role = Column(Integer,
                     server_default=id_role_seq.next_value(),
                     primary_key=True)
    name = Column(String(10))