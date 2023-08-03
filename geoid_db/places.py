from sqlalchemy import select
from sqlalchemy.orm import Session
from geoid_db.schema import Queries, Places
from geoid_db._processing import serialize


def list_places(
  session: Session, *, limit: int=10, offset: int=0
):
  statement = select(Places) \
              .order_by(Places.id.desc()) \
              .limit(limit) \
              .offset(offset)

  return serialize(session.scalars(statement).all())