# Copyright (c) 2023 Mifuyu (mifuyutsuki@proton.me)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from sqlalchemy import types
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List, Optional


class Base(DeclarativeBase):
  def asdict(self):
    #: Source: https://stackoverflow.com/a/1960546
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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
  location_name : Mapped[str]             = mapped_column(types.Unicode(255), index=True)
  location_type : Mapped[Optional[str]]   = mapped_column(types.String(255))
  latitude      : Mapped[float]           = mapped_column(types.DECIMAL(10, 7))
  longitude     : Mapped[float]           = mapped_column(types.DECIMAL(10, 7))
  province_id   : Mapped[Optional[int]]   = mapped_column(types.Integer())
  province_name : Mapped[Optional[str]]   = mapped_column(types.String(255))
  city_id       : Mapped[Optional[int]]   = mapped_column(types.Integer())
  city_name     : Mapped[Optional[str]]   = mapped_column(types.String(255))
  district_id   : Mapped[Optional[int]]   = mapped_column(types.Integer())
  district_name : Mapped[Optional[str]]   = mapped_column(types.String(255))
  village_id    : Mapped[Optional[int]]   = mapped_column(types.BigInteger())
  village_name  : Mapped[Optional[str]]   = mapped_column(types.String(255))
  postal_code   : Mapped[Optional[int]]   = mapped_column(types.Integer())
  rating        : Mapped[Optional[float]] = mapped_column(types.DECIMAL(3, 2))
  reviews       : Mapped[Optional[int]]   = mapped_column(types.Integer())
  description   : Mapped[Optional[str]]   = mapped_column(types.UnicodeText())
  location_link : Mapped[str]             = mapped_column(types.String(1023))

  query_id: Mapped[int] = mapped_column(ForeignKey('queries.id'))
  query: Mapped['Queries'] = relationship(back_populates='results')