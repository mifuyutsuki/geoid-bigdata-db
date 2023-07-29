from flask import request, abort
from geoid_db import app
from geoid_db import queries
from geoid_db import session
import sys


def _get_or_404(get):
  if get is None:
    abort(404)
  else:
    return get
  

@app.errorhandler(404)
def handle_404(e):
  return {
    'message': 'Path not found.'
  }, 404


@app.get('/queries')
def list_queries():
  offset = request.args.get('offset')
  offset = int(offset) if offset else 0

  with session.begin() as s:
    return _get_or_404(queries.list_queries(s, offset=offset))


@app.get('/queries/<int:id>')
def get_queries(id):
  with session.begin() as s:
    return _get_or_404(queries.from_id(id, s))


@app.get('/queries/<int:id>/results')
def list_places(id):
  with session.begin() as s:
    return _get_or_404(queries.list_places(id, s))


@app.post('/queries')
def add_queries():
  request_data = request.get_json()
  with session.begin() as s:
    return _get_or_404(queries.add(request_data))


@app.delete('/queries/<int:id>')
def delete_queries(id):
  with session.begin() as s:
    queries.delete(id)
  return ''


if __name__ == '__main__':
  try:
    debug = sys.argv[1].lower() != 'prod'
  except IndexError:
    debug = True
  app.run(debug=debug)