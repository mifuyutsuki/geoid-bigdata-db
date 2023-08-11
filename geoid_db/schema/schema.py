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


from sqlalchemy.orm import Session
from .consts import Keys, Status
from .tables import Queries, Places, Base


def init(engine):
  Base.metadata.create_all(engine, checkfirst=True)


def add(query_object: dict, session: Session):
  if query_object.get(Keys.QUERY_KEYWORD) is None:
    return
  if query_object.get(Keys.QUERY_STATUS) != Status.QUERY_COMPLETE:
    return
  if query_object.get(Keys.QUERY_RESULTS) is None:
    return
  if len(query_object.get(Keys.QUERY_RESULTS)) <= 0:
    return
  
  session.add(_build(query_object))


def _build(query_object: dict):
  queries = Queries(
    term      = query_object[Keys.QUERY_TERM],
    location  = query_object[Keys.QUERY_LOCATION],
    keyword   = query_object[Keys.QUERY_KEYWORD],
    lang      = query_object[Keys.QUERY_LANG],
    timestamp = query_object[Keys.QUERY_TIMESTAMP]
  )

  for query_result in query_object[Keys.QUERY_RESULTS]:
    queries.results.append(Places(
      location_name = query_result[Keys.LOCATION_NAME],
      location_type = query_result[Keys.LOCATION_TYPE],
      latitude      = query_result[Keys.LATITUDE],
      longitude     = query_result[Keys.LONGITUDE],
      province_id   = query_result[Keys.PROVINCE_ID],
      province_name = query_result[Keys.PROVINCE_NAME],
      city_id       = query_result[Keys.CITY_ID],
      city_name     = query_result[Keys.CITY_NAME],
      district_id   = query_result[Keys.DISTRICT_ID],
      district_name = query_result[Keys.DISTRICT_NAME],
      village_id    = query_result[Keys.VILLAGE_ID],
      village_name  = query_result[Keys.VILLAGE_NAME],
      postal_code   = query_result[Keys.POSTAL_CODE],
      rating        = query_result[Keys.RATING],
      reviews       = query_result[Keys.REVIEWS],
      description   = query_result[Keys.DESCRIPTION],
      location_link = query_result[Keys.LOCATION_LINK]
    ))

  return queries