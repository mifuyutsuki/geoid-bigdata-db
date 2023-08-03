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