import sqlite3
import flask


def database_connection(app: flask.Flask) -> sqlite3.Connection:
    if (database := getattr(flask.g, '_database', None)) is None:
        database = flask.g._database = sqlite3.connect(app.config["DATABASE_PATH"])
    database.row_factory = lambda c, r: dict((c.description[i][0], value) for i, value in enumerate(r))
    return database


def initialize_database(app: flask.Flask):
    database = database_connection(app)
    with app.open_resource(app.config['DATABASE_SCHEMA_PATH'], 'r') as file:
        database.executescript(file.read())