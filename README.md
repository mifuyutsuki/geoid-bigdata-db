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
* `/places`: List of places obtained by GeoID queries.
* `/apidocs`: API documentation.

## Requirements

* Python 3.11 or later
* SQLAlchemy 2.0 or later
* Flask
* Flasgger
* python-dotenv

In addition, by default, GeoID Database API connects to a MySQL 8.0 database using the PyMySQL connector, with which this API has been tested. MySQL is downloaded and configured separately. PyMySQL is included in `requirements.txt`.

## Setup

The following command-line setup is for Windows. Steps should be similar for Unix/macOS (replace `py` with `python3`, `copy` with `cp`, etc.)

1. Clone/download this repository and go (`cd`) to the cloned repository's path

   ```cmd
   git clone https://github.com/mifuyutsuki/geoid-bigdata-db
   cd geoid-bigdata-db
   ```

2. Create and activate virtual environment (`venv`)

   Using virtual environments avoids dependency conflicts with your other Python applications and projects.

   ```cmd
   py -m venv .venv
   .venv\scripts\activate.bat
   ```

3. Install dependencies listed in `requirements.txt`

   ```cmd
   pip install -r requirements.txt
   ```

4. Set up environment variables `.env` (example given by `example.env`)

   **This file contains your database credentials.** The following example copies `example.env` and launches Visual Studio Code (`code`) for editing.

   ```cmd
   copy example.env .env
   code .env
   ```

5. Launch API

   ```cmd
   flask --app geoid_db run
   ```

Servers such as Waitress (downloaded separately) can be used to launch the database API in a production environment:

```cmd
waitress-serve --host 127.0.0.1 --call geoid_db:create_app
```
