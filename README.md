# GeoID Database API

Simple database API for the GeoID program.

## About

GeoID Database API (`geoid-db` or `geoid-bigdata-db`) creates a RESTful interface to an external database to store data obtained by the GeoID program (`geoid-bigdata`).

By default, GeoID uses MySQL with the PyMySQL connector. PyMySQL is provided in `requirements.txt`.

GeoID Database API is created as part of an internship program.

## Endpoints

* `/queries`: List GeoID queries.
* `/queries/<id>`: Show information on a GeoID query with id `id`, which is assigned by the external database.
* `/queries/<id>/results`: Show places associated with GeoID query of id `id`.

## Setup

First, clone this repository to a path of your choosing, then in said path create a virtual environment. For example, in PowerShell:

```bash
git clone https://github.com/mifuyutsuki/geoid-bigdata-db
cd geoid-bigdata-db
python -m venv .venv
./.venv/Scripts/Activate.ps1
python -m pip install -e .
```

Before launching the API, make sure to set up a `.env` file with your database host and credentials. An example is given by `example.env`. Then you can launch the API in debug mode:

```bash
python -m geoid_db
```
