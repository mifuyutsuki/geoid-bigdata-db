from sqlalchemy import create_engine

import tomllib
from urllib.parse import quote_plus


ENGINE = '%(use_backend)s+%(use_driver)s://%(username)s:%(password)s@%(host)s:%(port)s/%(dbname)s'


def connect(*, echo=False, config_file='config.toml'):
  """
  Connect to database and return an SQLAlchemy database engine instance.

  By default, the file config.toml in the active path is used.

  Kwargs:
      echo (bool): Echo SQL statements emitted by the database engine
      config_file (str): Filename of the config TOML file

  Returns:
      New database engine instance
  """

  config_db = _load_config_db(config_file)
  return create_engine(ENGINE % config_db, echo=echo)


def _load_config_db(config_file: str='config.toml'):
  """
  Load database configuration from a config TOML file for use in connect().

  Args:
      config_file (str): Filename of the config TOML file

  Returns:
      Dict of config.toml table [database]
  """

  with open(config_file, 'rb') as f:
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