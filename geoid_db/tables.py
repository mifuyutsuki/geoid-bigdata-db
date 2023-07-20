from sqlalchemy import types
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from typing import List, Optional


class Base(DeclarativeBase):
  pass


class Queries(Base):
  __tablename__ = 'queries'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  term      : Mapped[str] = mapped_column(types.String(255), index=True)
  location  : Mapped[str] = mapped_column(types.String(255), index=True)
  keyword   : Mapped[str] = mapped_column(types.String(255))
  lang      : Mapped[str] = mapped_column(types.String(2))
  timestamp : Mapped[int] = mapped_column(types.BigInteger(), index=True)

  results: Mapped[List['Places']] = relationship(
    back_populates='query', cascade='all, delete-orphan'
  )


class Places(Base):
  __tablename__ = 'places'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  location_name : Mapped[str]             = mapped_column(types.Unicode(255))
  location_type : Mapped[Optional[str]]   = mapped_column(types.String(255))
  latitude      : Mapped[float]           = mapped_column(types.DECIMAL(10, 7))
  longitude     : Mapped[float]           = mapped_column(types.DECIMAL(10, 7))
  province_id   : Mapped[int]             = mapped_column(types.Integer())
  province_name : Mapped[str]             = mapped_column(types.String(255))
  city_id       : Mapped[int]             = mapped_column(types.Integer())
  city_name     : Mapped[str]             = mapped_column(types.String(255))
  district_id   : Mapped[int]             = mapped_column(types.Integer())
  district_name : Mapped[str]             = mapped_column(types.String(255))
  village_id    : Mapped[int]             = mapped_column(types.BigInteger())
  village_name  : Mapped[str]             = mapped_column(types.String(255))
  postal_code   : Mapped[int]             = mapped_column(types.Integer())
  rating        : Mapped[Optional[float]] = mapped_column(types.DECIMAL(3, 2))
  reviews       : Mapped[Optional[int]]   = mapped_column(types.Integer())
  description   : Mapped[Optional[str]]   = mapped_column(types.UnicodeText())
  location_link : Mapped[str]             = mapped_column(types.String(1023))

  query: Mapped['Queries'] = relationship(back_populates='results')