from flask import Flask
from flask import request
from geoid_api import queries

app = Flask(__name__)

@app.get('/queries/')
def get_queries_list():
  offset = request.args.get('q')
  offset = int(offset) if offset else 0
  return queries.get_list(offset=offset)


if __name__ == '__main__':
  app.run(debug=True)