from sqlalchemy import Engine
from geoid_db import commands


def _dictify(objects):
  results = [dict() for i in range(len(objects))]
  for index, table in enumerate(objects):
    results[index].update(table.asdict())
  return results


def get_queries_list(engine: Engine, *, limit: int=20, offset: int=0):
  objects = commands.get_queries_list(engine, limit=limit, offset=offset)
  return _dictify(objects)