from geoid_db.connect import connect

class GeoidEngine:
  def __init__(self, *, echo=False, use_config='config.toml'):
    self._engine = connect(echo=echo, config_file=use_config)

  @property
  def engine(self):
    return self._engine

_engine_instance = GeoidEngine()
engine = _engine_instance.engine