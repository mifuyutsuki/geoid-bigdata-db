from geoid_api import engine as engine
from geoid_api import _commands as commands


def get_list(limit: int=20, offset: int=0):
  return commands.get_queries_list(engine.engine, limit=limit, offset=offset)