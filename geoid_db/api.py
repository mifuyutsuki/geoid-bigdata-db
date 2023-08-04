# Copyright (c) 2023 mifuyutsuki

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from flask import request, abort
from flasgger import swag_from
from geoid_db import app
from geoid_db import queries, places
from geoid_db import session
from geoid_db._processing import content, content_paged
from werkzeug.exceptions import HTTPException
from http import HTTPStatus


def _get_or_404(get):
  if get is None:
    abort(HTTPStatus.NOT_FOUND, 'Database entry does not exist.')
  else:
    return get


def _get_start_limit():
  start = request.args.get('start')
  start = int(start) if start else 0
  if start < 0:
    abort(HTTPStatus.BAD_REQUEST, 'Start parameter cannot be a negative number.')

  limit = request.args.get('limit')
  limit = int(limit) if limit else 10
  if limit < 1:
    abort(HTTPStatus.BAD_REQUEST, 'Limit parameter cannot be less than one.')

  return start, limit
  

@app.errorhandler(HTTPException)
def handle_http_errors(e):
  return {
    'error': {
      'code': e.code,
      'name': e.name,
      'description': e.description
    }
  }, e.code


# =============================================================================
# =============================================================================


@app.get('/queries')
@swag_from('apidocs/queries_get.yml')
def list_queries():
  start, limit = _get_start_limit()
  location     = request.args.get('location')
  term         = request.args.get('term')

  with session.begin() as s:
    get = _get_or_404(
      queries.list_queries(
        s, location=location, term=term,
        offset=start, limit=limit
      )
    )
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
def list_queries_results(id):
  start, limit = _get_start_limit()

  with session.begin() as s:
    get = _get_or_404(queries.list_places(id, s, offset=start, limit=limit))
  return content_paged(get, limit=limit, start=start, id=id), HTTPStatus.OK


@app.delete('/queries/<int:id>')
@swag_from('apidocs/queries_id_delete.yml')
def delete_queries(id):
  with session.begin() as s:
    queries.delete(id, s)
  return '', HTTPStatus.NO_CONTENT


# =============================================================================
# =============================================================================


@app.get('/places')
@swag_from('apidocs/places_get.yml')
def list_places():
  start, limit = _get_start_limit()

  with session.begin() as s:
    get = _get_or_404(places.list_places(s, offset=start, limit=limit))
  return content_paged(get, limit=limit, start=start), HTTPStatus.OK