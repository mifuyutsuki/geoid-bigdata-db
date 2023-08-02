from flask import request, abort, url_for
from flasgger import swag_from
from geoid_db import app
from geoid_db import queries
from geoid_db import session
from werkzeug.exceptions import HTTPException
from http import HTTPStatus


def _get_or_404(get):
  if get is None:
    abort(HTTPStatus.NOT_FOUND, 'Database entry does not exist.')
  else:
    return get


def content_paged(results, *, limit=10, start=0, **kwargs):
  response_body = content(results, **kwargs)

  if isinstance(results, list):
    results_len = len(results)

    prev_start = max(start - limit, 0)
    if start > 0:
      response_body['_links'].update({
        'prev': {'href': url_for(request.endpoint, limit=limit, start=prev_start, **kwargs)}
      })

    next_start = start + limit
    if results_len >= limit:
      response_body['_links'].update({
        'next': {'href': url_for(request.endpoint, limit=limit, start=next_start, **kwargs)}
      })

    response_body.update({
      'size': len(results),
      'limit': limit,
      'start': start
    })

  return response_body


def content(results, **kwargs):
  return {
    '_links': {
      'self': {'href': url_for(request.endpoint, **kwargs, **request.args.to_dict())}
    },
    'results': results
  }


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
  start = request.args.get('start')
  start = int(start) if start else 0
  if start < 0:
    abort(HTTPStatus.BAD_REQUEST, 'Start parameter cannot be a negative number.')
  
  limit = request.args.get('limit')
  limit = int(limit) if limit else 10
  if limit < 1:
    abort(HTTPStatus.BAD_REQUEST, 'Limit parameter cannot be less than one.')

  with session.begin() as s:
    get = _get_or_404(queries.list_queries(s, limit=limit, offset=start))
  return content_paged(get, limit=limit, start=start), HTTPStatus.OK


@app.post('/queries')
@swag_from('apidocs/queries_post.yml')
def add_queries():
  request_data = request.get_json()
  with session.begin() as s:
    get = _get_or_404(queries.add(request_data))
  return content(get), HTTPStatus.CREATED


@app.get('/queries/<int:id>')
@swag_from('apidocs/queries_id_get.yml')
def get_queries(id):
  with session.begin() as s:
    get = _get_or_404(queries.from_id(id, s))
  return content(get, id=id), HTTPStatus.OK


@app.get('/queries/<int:id>/results')
@swag_from('apidocs/results_get.yml')
def list_places(id):
  start = request.args.get('start')
  start = int(start) if start else 0
  if start < 0:
    abort(HTTPStatus.BAD_REQUEST, 'Start parameter cannot be a negative number.')
  
  limit = request.args.get('limit')
  limit = int(limit) if limit else 10
  if limit < 1:
    abort(HTTPStatus.BAD_REQUEST, 'Limit parameter cannot be less than one.')

  with session.begin() as s:
    get = _get_or_404(queries.list_places(id, s, limit=limit, offset=start))
  return content_paged(get, limit=limit, start=start, id=id), HTTPStatus.OK


@app.delete('/queries/<int:id>')
@swag_from('apidocs/queries_id_delete.yml')
def delete_queries(id):
  with session.begin() as s:
    queries.delete(id, s)
  return '', HTTPStatus.NO_CONTENT