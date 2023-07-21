from sqlalchemy import create_engine

import tomllib
from urllib.parse import quote_plus


ENGINE = '%(use_backend)s+%(use_driver)s://%(username)s:%(password)s@%(host)s:%(port)s/%(dbname)s'


def connect(echo=False):
  """
  Connect to database using information given by config.toml.

  Returns:
      New database engine instance
  """

  config_db = _load_config_db()
  return create_engine(ENGINE % config_db, echo=echo)


def _load_config_db():
  """
  Load database configuration from config.toml for use in connect().

  Returns:
      Dict of config.toml table [database]
  """

  with open('config.toml', 'rb') as f:
    config = tomllib.load(f)
  
  config_db = config['database']
  for key in config_db.keys():
    if type(config_db[key]) is str:
      config_db[key] = quote_plus(config_db[key])

  username  = config_db['username']
  host      = config_db['host']
  port      = config_db['port']
  print(f'Connecting to database: {username}@{host}:{port}')

  return config_db