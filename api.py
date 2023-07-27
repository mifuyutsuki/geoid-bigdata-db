from flask import Flask
from flask import request
from geoid_api import commands
import sys

app = Flask(__name__)

@app.get('/queries')
def get_queries_list():
  offset = request.args.get('offset')
  offset = int(offset) if offset else 0
  return commands.get_queries_list(offset=offset)

@app.get('/queries/<int:id>')
def get_queries_one(id):
  return commands.get_queries_from_id(id)

@app.get('/queries/<int:id>/results')
def get_places_from_queries(id):
  return commands.get_places_from_queries_id(id)

@app.post('/queries')
def post_from_json():
  request_data = request.get_json()
  return commands.post_queries(request_data)


@app.delete('/queries/<int:id>')
def delete_queries(id):
  return commands.delete_queries(id)


if __name__ == '__main__':
  try:
    debug = sys.argv[1].lower() != 'prod'
  except IndexError:
    debug = True
  app.run(debug=debug)