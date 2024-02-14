from src.db.config import database_connection
from src.db.member import create

from flask import Blueprint, request, redirect, url_for, current_app


routes = Blueprint('Member', __name__, url_prefix='/member')


@routes.post('/create')
def create_member():
    database = database_connection(current_app)
    try: # making a transaction, make sure we always commit
        team_id, name = (request.form[key] for key in ('id', 'name'))
        color = request.form.get('color')
        create(database, team_id, name, color)
    except Exception as error:
        return redirect(url_for('index', error=error))
    finally:
        database.commit()

    return redirect(url_for('Team.view_team', rowid=team_id))