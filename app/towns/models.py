from sqlalchemy import Column, Integer, String, Text, ForeignKey, Sequence
# from app.app import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.countries.models import Country

Base = declarative_base()


class Town(Base):
    __tablename__ = 'towns'

    # id_town_seq = Sequence('towns_id_town_seq', metadata=Base.metadata)

    id_town = Column(Integer,
                     # server_default=id_town_seq.next_value(),
                     primary_key=True)
    name = Column(String(40), nullable=False)
    description = Column(Text)
    url_photo = Column(Text)
    id_country = Column(Integer, ForeignKey(Country.id_country))
    country = relationship(Country)
