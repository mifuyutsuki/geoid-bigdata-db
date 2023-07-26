from geoid_db.tables import Queries, Places
from geoid_db.constants import Keys, Status

from sqlalchemy import select
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from collections.abc import Sequence
import json


def get_queries_list(engine: Engine, limit: int=10, offset: int=0):
  statement = select(Queries) \
              .order_by(Queries.id) \
              .limit(limit) \
              .offset(offset)
  
  with Session(engine) as session:
    return session.scalars(statement).all()


def get_places_from_queries_id(queries_id: int, engine: Engine):
  """
  Get places associated with a Queries table entry `id`.

  Args:
      queries_id (int): Queries table ID
      engine (Engine): Database engine instance
  
  Returns:
      Sequence of combined Queries-Places
  """

  statement = select(Queries, Places) \
              .join(Places, Queries.results) \
              .where(Queries.id == queries_id) \
              .order_by(Places.id)

  with Session(engine) as session:
    return session.execute(statement).all()


def get_queries_from_id(id: int, engine: Engine):
  """
  Get a queries entry associated with ID `id`.

  Args:
      id (int): Queries table ID
      engine (Engine): Database engine instance
  
  Returns:
      Queries row associated with ID `id`, or `None` if not found
  """
  
  statement = select(Queries) \
    .where(Queries.id == id)
  
  with Session(engine) as session:
    return session.scalars(statement).first()


def get_queries_from_ids(ids: Sequence[int], engine: Engine):
  """
  Get queries entries associated with sequence of IDs `ids`.

  Args:
      ids (Sequence[int]): Sequence of Queries table IDs
      engine (Engine): Database engine instance
  
  Returns:
      Sequence of Queries rows associated with IDs `ids`
  """

  statement = select(Queries) \
    .where(Queries.id.in_(ids))
  
  with Session(engine) as session:
    return session.scalars(statement).all()
  

def get_ids_from_location(location: str, engine: Engine):
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
  
  with Session(engine) as session:
    return session.scalars(statement).all()
  

def get_ids_from_term(term: str, engine: Engine):
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
  
  with Session(engine) as session:
    return session.scalars(statement).all()


def post_from_file(filename: str, engine: Engine):
  """
  Add a queries data JSON file to the geoid database.

  Args:
      filename (str): JSON file name containing queries data
      engine (Engine): Database engine instance
  """

  with open(filename, 'r', encoding='UTF-8') as f:
    queries_data = json.load(f)

  with Session(engine) as session:
    for query_object in queries_data:
      _add_entry(query_object, session)
    session.commit()
  

def _add_entry(query_object: dict, session: Session):
  if query_object.get(Keys.QUERY_KEYWORD) is None:
    return
  if query_object.get(Keys.QUERY_STATUS) != Status.QUERY_COMPLETE:
    return
  if query_object.get(Keys.QUERY_RESULTS) is None:
    return
  if len(query_object.get(Keys.QUERY_RESULTS)) <= 0:
    return
  
  session.add(_create_entry(query_object))


def _create_entry(query_object: dict):
  queries = Queries(
    term      = query_object[Keys.QUERY_TERM],
    location  = query_object[Keys.QUERY_LOCATION],
    keyword   = query_object[Keys.QUERY_KEYWORD],
    lang      = query_object[Keys.QUERY_LANG],
    timestamp = query_object[Keys.QUERY_TIMESTAMP]
  )

  for query_result in query_object[Keys.QUERY_RESULTS]:
    queries.results.append(Places(
      location_name = query_result[Keys.LOCATION_NAME],
      location_type = query_result[Keys.LOCATION_TYPE],
      latitude      = query_result[Keys.LATITUDE],
      longitude     = query_result[Keys.LONGITUDE],
      province_id   = query_result[Keys.PROVINCE_ID],
      province_name = query_result[Keys.PROVINCE_NAME],
      city_id       = query_result[Keys.CITY_ID],
      city_name     = query_result[Keys.CITY_NAME],
      district_id   = query_result[Keys.DISTRICT_ID],
      district_name = query_result[Keys.DISTRICT_NAME],
      village_id    = query_result[Keys.VILLAGE_ID],
      village_name  = query_result[Keys.VILLAGE_NAME],
      postal_code   = query_result[Keys.POSTAL_CODE],
      rating        = query_result[Keys.RATING],
      reviews       = query_result[Keys.REVIEWS],
      description   = query_result[Keys.DESCRIPTION],
      location_link = query_result[Keys.LOCATION_LINK]
    ))

  return queries