from flask import request, abort
from geoid_db import app
from geoid_db import queries
from geoid_db import session
from werkzeug.exceptions import HTTPException


def _get_or_404(get):
  if get is None:
    abort(404)
  else:
    return get
  

@app.errorhandler(HTTPException)
def handle_http_errors(e):
  return {
    'error': {
      'code': e.code,
      'name': e.name,
      'description': e.description
    }
  }, e.code


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