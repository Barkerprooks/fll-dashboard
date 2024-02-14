from src.db.config import database_connection
from src.db.run import create, get, update_file, llsp3_file_format, modify_robot_slot, modify_title, remove

from flask import Blueprint, request, redirect, url_for, current_app
from semver import parse_version_info

import src.db.team as teams
import os


routes = Blueprint('Run', __name__, url_prefix='/run')


def prepare_file_path(group_name: str):
    group_path = os.path.join(current_app.config['LLSP3_UPLOAD_PATH'], group_name)
    if not os.path.isdir(group_path):
        os.makedirs(group_path)
    return group_path


@routes.post('/create')
def create_run():
    database = database_connection(current_app)
    try:
        team_id, robot_slot, title = (request.form[key] for key in ('id', 'robot_slot', 'title'))
        upload = request.files['upload']

        group_name = teams.get(database, team_id)['group_name']
        group_path = prepare_file_path(group_name)

        upload.save(os.path.join(group_path, llsp3_file_format(group_name, title, '0.0.1')))

        create(database, team_id, robot_slot, title)
    except Exception as error:
        return redirect(url_for('Team.view_team', rowid=team_id, error=error))
    finally:
        database.commit()

    return redirect(url_for('Team.view_team', rowid=team_id))


@routes.post('/update')
def update_run():
    database = database_connection(current_app)
    team_id, rowid = (request.form[key] for key in ('team_id', 'id'))
    try:
        upload = request.files['upload']


        group_name = teams.get(database, team_id)['group_name']
        group_path = prepare_file_path(group_name)
        run = get(database, rowid)

        version = parse_version_info(run['version'])

        version = version.bump_patch()
        if version.patch > 9:
            version = version.bump_minor()
        if version.minor > 9:
            version = version.bump_major()

        version = str(version)

        upload.save(os.path.join(group_path, llsp3_file_format(group_name, run['title'], version)))
        update_file(database, rowid, version)
    except Exception as error:
        return redirect(url_for('Team.view_team', rowid=team_id, error=error))
    finally:
        database.commit()

    return redirect(url_for('Team.view_team', rowid=team_id))

@routes.post('/modify')
def modify_run():
    database = database_connection(current_app)
    team_id, rowid = (request.form[key] for key in ('team_id', 'id'))
    try:
        robot_slot, title = (request.form.get(key) for key in ('robot_slot', 'title'))
        if robot_slot:
            modify_robot_slot(database, rowid, robot_slot)
        if title:
            modify_title(database, rowid, title)
    except Exception as error:
        return redirect(url_for('Team.view_team', rowid=team_id, error=error))
    finally:
        database.commit()

    return redirect(url_for('Team.view_team', rowid=team_id))

@routes.post('/remove')
def remove_run():
    database = database_connection(current_app)
    team_id, rowid = (request.form[key] for key in ('team_id', 'id'))
    try:
        remove(database, rowid)
    except Exception as error:
        return redirect(url_for('Team.view_team', rowid=team_id, error=error))
    finally:
        database.commit()

    return redirect(url_for('Team.view_team', rowid=team_id))