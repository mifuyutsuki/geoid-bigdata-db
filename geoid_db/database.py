from geoid_db import tables
from geoid_db.constants import Keys

from sqlalchemy.orm import Session

import json


def add_from_file(filename: str, engine):
  """
  Add a queries data JSON file to the geoid database.

  Args:
      filename (str): JSON file name containing queries data.
  """

  with open(filename, 'r', encoding='UTF-8') as f:
    queries_data = json.load(f)

  with Session(engine) as session:
    for query_object in queries_data:
      session.add(_create_entry(query_object))
    session.commit()
  

def _create_entry(query_object: dict):
  queries = tables.Queries(
    term      = query_object[Keys.QUERY_TERM],
    location  = query_object[Keys.QUERY_LOCATION],
    keyword   = query_object[Keys.QUERY_KEYWORD],
    lang      = query_object[Keys.QUERY_LANG],
    timestamp = query_object[Keys.QUERY_TIMESTAMP]
  )

  for query_result in query_object[Keys.QUERY_RESULTS]:
    queries.results.append(tables.Places(
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