from sqlalchemy import select
from sqlalchemy.orm import Session
from geoid_db.schema import Queries, Places
from geoid_db.schema import SchemaBase
from geoid_db.schema import add as add_entry
from collections.abc import Sequence


def exists(id: int, session: Session):
  statement = select(Queries.id) \
              .where(Queries.id == id)

  selected = session.scalars(statement).first()
  return selected is not None


def list_queries(session: Session, *, limit: int=20, offset: int=0) -> list[dict]:
  statement = select(Queries) \
              .order_by(Queries.id) \
              .limit(limit) \
              .offset(offset)

  return _dictify(session.scalars(statement).all())


def from_id(id: int, session: Session) -> list[dict]:
  statement = select(Queries) \
              .where(Queries.id == id)
  
  return _dictify(session.scalars(statement).first())


def search_location(location: str, session: Session):
  """
  Get Queries IDs associated with query location `location`.

  Args:
      location (str): Query location (case-insensitive)
      engine (Engine): Database engine instance
  
  Returns:
      Sequence of IDs
  """

  statement = select(Queries.id) \
              .where(Queries.location == location.lower())
  
  return session.scalars(statement).all()
  

def search_term(term: str, session: Session):
  """
  Get Queries IDs associated with query term `term`.

  Args:
      term (str): Query term (case-insensitive)
      engine (Engine): Database engine instance
  
  Returns:
      Sequence of IDs
  """

  statement = select(Queries.id) \
              .where(Queries.term == term.lower())
  
  return session.scalars(statement).all()
  

def list_places(id: int, session: Session) -> list[dict] | None:
  """
  Get places associated with a Queries table entry `id`.

  Args:
      queries_id (int): Queries table ID
      session (Session): Database session instance
  
  Returns:
      Sequence of combined Queries-Places
  """

  statement = select(Places) \
              .where(Places.query_id == id)

  if not exists(id, session):
    return None
  else:
    return _dictify(session.scalars(statement).all())


def add(data, session: Session) -> dict:
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


def _dictify(tables) -> list[dict] | dict | None:
  if tables is None:
    #: Pass None instead
    return None
  
  if isinstance(tables, Sequence):
    return _dictify_sequence(tables)
  elif isinstance(tables, SchemaBase):
    return _dictify_table(tables)
  else:
    raise ValueError(f'Cannot dictify object of type "{str(type(tables))}"')


def _dictify_table(table: SchemaBase) -> dict:
  return table.asdict()


def _dictify_sequence(tables: Sequence[SchemaBase]) -> list[dict]:
  results = [dict() for i in range(len(tables))]
  for index, table in enumerate(tables):
    results[index].update(table.asdict())
  return results