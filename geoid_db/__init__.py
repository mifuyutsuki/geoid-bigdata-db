from dotenv import load_dotenv
load_dotenv('.env')

from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URI = '%(DB_BACKEND)s://%(DB_USERNAME)s:%(DB_PASSWORD)s@%(DB_HOST)s/%(DB_NAME)s' % os.environ
engine = create_engine(DATABASE_URI)
session = sessionmaker(engine)

from geoid_db import api