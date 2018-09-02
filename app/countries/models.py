from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

# from app.app import db

Base = declarative_base()


class Country(Base):
    __tablename__ = 'country'
    id_country_seq = Sequence('country_id_country_seq', metadata=Base.metadata)

    id_country = Column(Integer, id_country_seq,
                        server_default=id_country_seq.next_value(),
                        primary_key=True)
    name = Column(String(40), nullable=False)
