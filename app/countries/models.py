from sqlalchemy import Column, Integer, String, Sequence
from app.app import db


class Country(db.Model):
    __tablename__ = 'countries'
    id_country_seq = Sequence('countries_id_country_seq', metadata=db.metadata)

    id_country = Column(Integer, id_country_seq,
                        server_default=id_country_seq.next_value(),
                        primary_key=True)
    name = Column(String(40), nullable=False)