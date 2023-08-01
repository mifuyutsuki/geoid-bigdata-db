from dotenv import load_dotenv
load_dotenv('.env')

from flask import Flask
from flasgger import Swagger
app = Flask(__name__)
swagger = Swagger(app, template_file='apidocs/template.yml')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URI = '%(DB_BACKEND)s://%(DB_USERNAME)s:%(DB_PASSWORD)s@%(DB_HOST)s/%(DB_NAME)s' % os.environ
engine = create_engine(DATABASE_URI)
session = sessionmaker(engine)

from geoid_db import api

def create_app():
  app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
  )
  return app