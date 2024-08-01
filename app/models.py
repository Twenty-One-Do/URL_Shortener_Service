import pytz
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class BaseUrl(Base):
    __tablename__ = 'base_urls'

    id = Column(Integer, primary_key=True)
    base_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    paths = relationship('Path', back_populates='base_url')

class Path(Base):
    __tablename__ = 'paths'

    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    expiration_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    base_url_id = Column(Integer, ForeignKey('base_urls.id'))

    base_url = relationship('BaseUrl', back_populates='paths')
    short_urls = relationship('ShortUrl', back_populates='path')

class ShortUrl(Base):
    __tablename__ = 'short_urls'

    id = Column(Integer, primary_key=True)
    short_url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    expiration_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    path_id = Column(Integer, ForeignKey('paths.id'))

    path = relationship('Path', back_populates='short_urls')
    stats = relationship('ShortUrlStat', back_populates='short_url')

class ShortUrlStat(Base):
    __tablename__ = 'short_url_stats'

    id = Column(Integer, primary_key=True)
    device_type = Column(String, nullable=False)
    click_time = Column(DateTime, default=datetime.now())
    ip = Column(String, nullable=False)
    short_url_id = Column(Integer, ForeignKey('short_urls.id'))

    short_url = relationship('ShortUrl', back_populates='stats')
