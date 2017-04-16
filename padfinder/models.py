from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()

post_tag = Table(
    'post_tag', Base.metadata,
    Column('post_id', BigInteger, ForeignKey('post.id')),
    Column('tag_id', BigInteger, ForeignKey('tag.id')),
)


class ApartmentPost(Base):
    __tablename__ = 'post'

    id = Column(BigInteger, primary_key=True)
    repost_of = Column(BigInteger)
    snapshot_ts = Column(DateTime)
    posted_ts = Column(DateTime)
    url = Column(String)
    region = Column(String)
    subregion = Column(String)
    title = Column(String)
    price = Column(Integer)
    bedrooms = Column(Integer)
    sqfeet = Column(Integer)
    neighborhood = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    available_date = Column(Date)
    tag_list = Column(String)

    tags = relationship('ApartmentTag', secondary=post_tag, backref='posts')
    commutes = relationship('Commute', backref='post')


class ApartmentTag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Destination(Base):
    __tablename__ = 'destination'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class TransitMode(Base):
    __tablename__ = 'transit_mode'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class DepartureTime(Base):
    __tablename__ = 'depart_time'
    id = Column(Integer, primary_key=True)
    ts = Column(DateTime)


class Commute(Base):
    __tablename__ = 'commute'

    id = Column(Integer, primary_key=True)
    post_id = Column(BigInteger, ForeignKey('post.id'))
    destination_id = Column(Integer, ForeignKey('destination.id'))
    transit_mode_id = Column(Integer, ForeignKey('transit_mode.id'))
    depart_time_id = Column(Integer, ForeignKey('depart_time.id'))
    distance = Column(String)
    duration = Column(String)
    distance_meters = Column(Float)
    duration_seconds = Column(Float)

    destination = relationship('Destination')
    transit_mode = relationship('TransitMode')
    depart_time = relationship('DepartureTime')
