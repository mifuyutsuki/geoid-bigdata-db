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


from sqlalchemy import select
from sqlalchemy.orm import Session
from geoid_db._processing import serialize
from geoid_db.schema import Queries, Places
from geoid_db.schema import add as add_entry


def exists(id: int, session: Session):
  statement = select(Queries.id) \
              .where(Queries.id == id)

  selected = session.scalars(statement).first()
  return selected is not None


def from_id(id: int, session: Session):
  statement = select(Queries) \
              .where(Queries.id == id)
  
  return serialize(session.scalars(statement).first())


def list_queries(
  session: Session,
  *,
  location: str=None,
  term: str=None,
  offset=0,
  limit=10
):
  selection = select(Queries)
  if location is not None:
    selection = selection.where(
      Queries.location.like(f'%{location.strip()}%')
    )
  if term is not None:
    selection = selection.where(
      Queries.term.like(f'%{term.strip()}%')
    )

  statement = (
    selection
    .order_by(Queries.id.desc())
    .limit(limit)
    .offset(offset)
  )

  return serialize(session.scalars(statement).all())
  

def list_places(id: int, session: Session, *, limit=10, offset=0):
  """
  Get places associated with a Queries table entry `id`.

  Args:
      queries_id (int): Queries table ID
      session (Session): Database session instance
  
  Returns:
      Sequence of combined Queries-Places
  """

  statement = select(Places) \
              .where(Places.query_id == id) \
              .order_by(Places.id) \
              .limit(limit) \
              .offset(offset)

  if not exists(id, session):
    return None
  else:
    return serialize(session.scalars(statement).all())


def add(data, session: Session):
  """
  Add a queries data to the geoid database.

  Args:
      data: JSON data containing queries data
      engine (Engine): Database engine instance
  """

  if not isinstance(data, list):
    raise ValueError('Queries data is not an array of objects')

  for query_object in data:
    add_entry(query_object, session)
  return {'number_created': len(data)}


def delete(id: int, session: Session):
  """
  Delete a queries data and its associated places from the geoid database.

  Args:
      id (int): Queries table ID
      engine (Engine): Database engine instance
  """
  
  statement = select(Queries) \
              .where(Queries.id == id)

  selected = session.scalars(statement).first()
  session.delete(selected)
  session.commit()