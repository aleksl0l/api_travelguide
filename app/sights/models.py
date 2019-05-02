from sqlalchemy import Column, Integer, String, REAL, Text, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base

from app.towns.models import Town

Base = declarative_base()


class Sights(Base):
    __tablename__ = 'sights'

    id_sight = Column(Integer, primary_key=True)
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

    def serialize(self):
        return {
            'id_town': self.id_town,
            'id_sight': self.id_sight,
            'name': self.name,
            'tags': self.tag,
            'cost': self.cost,
            'coordinate': [self.cord_lat, self.cord_long],
            'rating': self.rating,
            'type': self.type_sight,
            'photo_urls': self.urls,
            'web_site': self.web_site,
            'description': self.description,
            'history': self.history,
            'phone_number': self.phone_number,
        }
