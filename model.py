from sqlalchemy import Column, Integer, String, REAL, Text, ForeignKey, Sequence, ARRAY, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import re
import sqlalchemy.types as types


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


Base = declarative_base()


class Country(Base):
    __tablename__ = 'countries'
    id_country_seq = Sequence('countries_id_country_seq', metadata=Base.metadata)

    id_country = Column(Integer, id_country_seq,
                        server_default=id_country_seq.next_value(),
                        primary_key=True)
    name = Column(String(40), nullable=False)


class Town(Base):
    __tablename__ = 'towns'

    id_town_seq = Sequence('towns_id_town_seq', metadata=Base.metadata)

    id_town = Column(Integer,
                     server_default=id_town_seq.next_value(),
                     primary_key=True)

    name = Column(String(40), nullable=False)
    description = Column(Text)
    id_country = Column(Integer, ForeignKey('countries.id_country'))

    id_country_rel = relationship('Country', foreign_keys=[id_country])


class Sights(Base):
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
    urls = Column(ARRAY(Text))
    id_town_rel = relationship('Town', foreign_keys=[id_town])


class Roles(Base):
    __tablename__ = 'roles'

    id_role_seq = Sequence('roles_id_role_seq', metadata=Base.metadata)

    id_role = Column(Integer,
                     server_default=id_role_seq.next_value(),
                     primary_key=True)
    name = Column(String(10))


class Users(Base):
    __tablename__ = 'users'

    id_user_seq = Sequence('users_id_user_seq', metadata=Base.metadata)

    id_user = Column(Integer,
                     server_default=id_user_seq.next_value(),
                     primary_key=True)
    public_id = Column(String(36))
    name = Column(String(50), unique=True)
    password = Column(String(100))
    id_role = Column(Integer, ForeignKey('roles.id_role'))
    id_role_rel = relationship('Roles', foreign_keys=[id_role])


class Likes(Base):
    __tablename__ = 'likes'

    id_like_seq = Sequence('likes_id_like_seq', metadata=Base.metadata)

    id_like = Column(Integer,
                     server_default=id_like_seq.next_value(),
                     primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id_user'))
    id_sight = Column(Integer, ForeignKey('sights.id_sights'))
    value = Column(Integer, nullable=False)

    id_user_rel = relationship('Users', foreign_keys=[id_user])
    id_sights_rel = relationship('Sights', foreign_keys=[id_sight])
    UniqueConstraint('id_user', 'id_sight')
