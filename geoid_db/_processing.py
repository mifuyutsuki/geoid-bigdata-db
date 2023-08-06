# Copyright (c) 2023 Mifuyu (mifuyutsuki@proton.me)

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


from flask import request, url_for
from geoid_db.schema import SchemaBase
from collections.abc import Sequence


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


def serialize(tables):
  if tables is None:
    #: Pass None instead of throwing error
    return None
  
  if isinstance(tables, Sequence):
    return _serialize_sequence(tables)
  elif isinstance(tables, SchemaBase):
    return _serialize_table(tables)
  else:
    raise ValueError(f'Cannot dictify object of type "{str(type(tables))}"')


def _serialize_table(table: SchemaBase) -> dict:
  return table.asdict()


def _serialize_sequence(tables: Sequence[SchemaBase]) -> list[dict]:
  results = [dict() for i in range(len(tables))]
  for index, table in enumerate(tables):
    results[index].update(table.asdict())
  return results