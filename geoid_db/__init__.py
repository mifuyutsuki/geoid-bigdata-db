# Copyright (c) 2023 mifuyutsuki

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