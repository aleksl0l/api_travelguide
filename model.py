from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, REAL, Text, ForeignKey, Sequence, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import re
import sqlalchemy.types as types

class Point(types.UserDefinedType):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def get_col_spec(self, **kw):
        return 'POINT(%s,%s)' % (self.x, self.y)

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

db = SQLAlchemy()

Base = declarative_base()


class Country(Base, db.Model):
    __tablename__ = 'countries'
    id_country_seq = Sequence('countries_id_country_seq', metadata=Base.metadata)

    id_country = Column(Integer, id_country_seq,
                        server_default=id_country_seq.next_value(),
                        primary_key=True)
    name = Column(String(40), nullable=False)


class Town(Base, db.Model):
    __tablename__ = 'towns'

    id_town_seq = Sequence('towns_id_town_seq', metadata=Base.metadata)

    id_town = Column(Integer,
                     server_default=id_town_seq.next_value(),
                     primary_key=True)

    name = Column(String(40), nullable=False)
    description = Column(Text)
    id_country = Column(Integer, ForeignKey('countries.id_country'))

    id_country_rel = relationship('Country', foreign_keys=[id_country])


class Sights(Base, db.Model):
    __tablename__ = 'sights'

    id_sights_seq = Sequence('sights_id_sights_seq', metadata=Base.metadata)

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


    id_town_rel = relationship('Town', foreign_keys=[id_town])

# class Setsandwords(Base, db.Model):
#     __tablename__ = 'setsandwords'
#
#     set_id = Column(Integer, ForeignKey('sets.set_id'), primary_key=True)
#     word_id = Column(Integer, ForeignKey('words.word_id'), primary_key=True)
#
#     set_id_rel = relationship('Sets', foreign_keys=[set_id])
#     word_id_rel = relationship('Words', foreign_keys=[word_id])