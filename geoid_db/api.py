from flask import request, abort
from flasgger import swag_from
from geoid_db import app
from geoid_db import queries
from geoid_db import session
from werkzeug.exceptions import HTTPException


def _get_or_404(get):
  if get is None:
    abort(404, 'Database entry does not exist.')
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
@swag_from('apidocs/queries_get.yml')
def list_queries():
  offset = request.args.get('offset')
  offset = int(offset) if offset else 0
  if offset < 0:
    abort(400, 'Offset parameter cannot be a negative number.')
  
  show = request.args.get('show')
  show = int(show) if show else 20
  if show < 1:
    abort(400, 'Show parameter cannot be less than one.')

  with session.begin() as s:
    return _get_or_404(queries.list_queries(s, limit=show, offset=offset))


@app.post('/queries')
@swag_from('apidocs/queries_post.yml')
def add_queries():
  request_data = request.get_json()
  with session.begin() as s:
    return _get_or_404(queries.add(request_data))


@app.get('/queries/<int:id>')
@swag_from('apidocs/queries_id_get.yml')
def get_queries(id):
  with session.begin() as s:
    return _get_or_404(queries.from_id(id, s))


@app.get('/queries/<int:id>/results')
@swag_from('apidocs/results_get.yml')
def list_places(id):
  with session.begin() as s:
    return _get_or_404(queries.list_places(id, s))


@app.delete('/queries/<int:id>')
@swag_from('apidocs/queries_id_delete.yml')
def delete_queries(id):
  with session.begin() as s:
    queries.delete(id)
  return ''