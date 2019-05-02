from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.countries.models import Country

Base = declarative_base()


class Town(Base):
    __tablename__ = 'towns'

    id_town = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    description = Column(Text)
    url_photo = Column(Text)
    id_country = Column(Integer, ForeignKey(Country.id_country))
    country = relationship(Country)
