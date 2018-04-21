from sqlalchemy import Column, Integer, String, REAL, Text, ForeignKey, Sequence, ARRAY, UniqueConstraint
from sqlalchemy.orm import relationship
import re
import sqlalchemy.types as types
from app.app import db


class Point(types.UserDefinedType):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def get_col_spec(self, **kw):
        return '(%s,%s)' % (self.x, self.y)

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            lat = None
            long = None
            if value:
                m = re.match(r"\(([^)]+),([^)]+)\)", value)
                lat = m.group(1)
                long = m.group(2)
            return {'lat': lat, 'long': long}
        return process


class Sights(db.Model):
    __tablename__ = 'sights'

    id_sights_seq = Sequence('sights_id_sights_seq', metadata=db.metadata)

    id_sights = Column(Integer,
                       server_default=id_sights_seq.next_value(),
                       primary_key=True)
    name = Column(String(100), nullable=False)
    tag = Column(ARRAY(Text))
    cost = Column(REAL)
    id_town = Column(Integer, ForeignKey('towns.id_town'))
    coordinate = Column(Point)
    rating = Column(REAL)
    type_sight = Column(Text)
    urls = Column(ARRAY(Text))
    web_site = Column(Text)
    description = Column(Text)
    history = Column(Text)
    phonenumber = Column(String(20))
    id_town_rel = relationship('Town', foreign_keys=[id_town])