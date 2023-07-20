from sqlalchemy import create_engine

import tomllib
from urllib.parse import quote_plus


ENGINE = '%(use_backend)s+%(use_driver)s://%(username)s:%(password)s@%(host)s:%(port)s/%(dbname)s'


def connect():
  """
  Connect to database using information given by config.toml.

  Returns:
      New database engine instance
  """

  try:
    config = _load_config()
  except FileNotFoundError:
    print(f'Could not find "config.toml" in active directory')
    return

  config_db = config['database']
  for key in config_db.keys():
    if type(config_db[key]) is str:
      config_db[key] = quote_plus(config_db[key])

  username  = config_db['username']
  host      = config_db['host']
  port      = config_db['port']
  print(f'Connecting to database: {username}@{host}:{port}')

  return create_engine(ENGINE % config_db)


def _load_config():
  """
  Load configuration file config.toml in active (`__main__`) directory.

  Returns:
      Dict parsed from config.toml
  """

  with open('config.toml', 'rb') as f:
    return tomllib.load(f)