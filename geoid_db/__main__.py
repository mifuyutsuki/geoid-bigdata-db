from geoid_db import app
import sys

if __name__ == '__main__':
  try:
    debug = sys.argv[1].lower() != 'prod'
  except IndexError:
    debug = True
  app.run(debug=debug)