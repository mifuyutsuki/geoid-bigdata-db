# GeoID Database API

Simple database API for GeoID (`geoid-bigdata`).

## About

GeoID Database API (`geoid-db` or `geoid-bigdata-db`) is a Flask-based RESTful interface for database of queries obtained through the GeoID program ([`geoid-bigdata`](https://github.com/mifuyutsuki/geoid-bigdata)).

By default, GeoID uses MySQL with the PyMySQL connector. PyMySQL is included in `requirements.txt`.

GeoID Database API is created as part of an internship program.

## Endpoints

* `/queries`: List of GeoID queries.
* `/queries/<id>`: Information on a GeoID query with id `id`, which is assigned by the external database.
* `/queries/<id>/results`: Places associated with GeoID query of id `id`.
* `/apidocs`: API documentation powered by Swagger (via Flasgger).

## Requirements

* Python 3.11 or later
* SQLAlchemy 2.0 or later
* Flask
* Flasgger
* python-dotenv

In addition, by default, GeoID Database API connects to a MySQL 8.0 database using the PyMySQL connector, with which this API has been tested. MySQL is downloaded and configured separately. PyMySQL is included in `requirements.txt`.

## Setup

First, clone this repository to a path of your choosing, then create a virtual environment in the path, to prevent dependency conflicts with your other Python applications and projects. For example:

```cmd
git clone https://github.com/mifuyutsuki/geoid-bigdata-db
cd geoid-bigdata-db
py -m venv .venv
./.venv/Scripts/Activate.bat
pip install .
```

Optionally, use `pip install -e .` to install an editable package.

Before launching the API, make sure to set up a `.env` file with your database host and credentials. An example is given by `example.env`. Then you can launch the API in debug mode:

```cmd
py -m geoid_db
```
