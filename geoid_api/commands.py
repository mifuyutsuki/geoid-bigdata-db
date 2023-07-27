from geoid_api import engine
from geoid_db import commands
from http import HTTPStatus


def get_queries_list(*, limit: int=20, offset: int=0) -> tuple[list[dict], HTTPStatus]:
  objects = commands.get_queries_list(engine, limit=limit, offset=offset)
  return _dictify(objects), HTTPStatus.OK


def get_queries_from_id(id: int) -> tuple[list[dict], HTTPStatus]:
  objects = commands.get_queries_from_id(id, engine)
  if objects is None:
    return '', HTTPStatus.NOT_FOUND
  else:
    return objects.asdict(), HTTPStatus.OK
  

def get_places_from_queries_id(id: int) -> tuple[list[dict], HTTPStatus]:
  objects = commands.get_places_from_queries_id(id, engine)
  return _dictify(objects), HTTPStatus.OK


def post_queries(data) -> tuple[dict, HTTPStatus]:
  if isinstance(data, list):
    output = {'number_created': len(data)}
  else:
    return '', HTTPStatus.BAD_REQUEST
  
  commands.post_from_data(data, engine)
  return output, HTTPStatus.CREATED


def delete_queries(id) -> tuple[str, HTTPStatus]:
  commands.delete_queries(id, engine)
  return '', HTTPStatus.NO_CONTENT


def _dictify(objects) -> list[dict]:
  results = [dict() for i in range(len(objects))]
  for index, table in enumerate(objects):
    results[index].update(table.asdict())
  return results