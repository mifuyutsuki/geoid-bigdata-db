import mysql.connector
import getpass


def connect(user: str, host: str='localhost', db: str='geoid'):
  print(f'Connecting to MySQL database {db} at {host} as {user}')
  return mysql.connector.connect(
    user=user,
    password=getpass.getpass(),
    host=host,
    database=db
  )