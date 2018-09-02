from sqlalchemy import Column, Integer, String, REAL, Text, ForeignKey, ARRAY
# from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.towns.models import Town

# from app.app import db

Base = declarative_base()


class Sights(Base):
    __tablename__ = 'sights'

    # id_sights_seq = Sequence('sights_id_sights_seq', metadata=Base.metadata)

    id_sight = Column(Integer,
                      # server_default=id_sights_seq.next_value(),
                      primary_key=True)
    name = Column(String(100), nullable=False)
    tag = Column(ARRAY(Text))
    cost = Column(REAL)
    id_town = Column(Integer, ForeignKey(Town.id_town))
    cord_lat = Column(Integer)
    cord_long = Column(Integer)
    rating = Column(REAL)
    type_sight = Column(Text)
    urls = Column(ARRAY(Text))
    web_site = Column(Text)
    description = Column(Text)
    history = Column(Text)
    phone_number = Column(String(20))
    # id_town_rel = relationship('Town', foreign_keys=[id_town])
