from sqlalchemy import Column, Integer, String, Text, ForeignKey, Sequence
from app.app import db


class Town(db.Model):
    __tablename__ = 'towns'

    id_town_seq = Sequence('towns_id_town_seq', metadata=db.metadata)

    id_town = Column(Integer,
                     server_default=id_town_seq.next_value(),
                     primary_key=True)
    name = Column(String(40), nullable=False)
    description = Column(Text)
    url_photo = Column(Text)
    id_country = Column(Integer, ForeignKey('country.id_country'))
    # id_country_rel = relationship('Country', foreign_keys=[id_country])