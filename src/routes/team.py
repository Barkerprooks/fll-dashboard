from src.db.team import create, get, modify_group_name, modify_robot_name, remove, PUBLIC_FIELDS
from src.db.config import database_connection
from src.db.query import nav, runs

from flask import Blueprint, request, current_app, render_template, redirect, url_for

import os

routes = Blueprint('Team', __name__, url_prefix='/team')


@routes.get('/<int:rowid>')
def view_team(rowid):
    database = database_connection(current_app)
    team = get(database, rowid)
    return render_template(
        "team.html", 
        page=team['group_name'],
        team=team,
        runs=runs(database, rowid),
        nav=nav(database),
        version=current_app.config['VERSION'], 
        error=request.args.get('error'),
        modal=request.args.get('modal'),
        edit=int(request.args.get('edit', 0))
    )


@routes.post('/create')
def create_team():
    database = database_connection(current_app)
    image_upload_path = current_app.config['IMAGE_UPLOAD_PATH']
    try: # making a transaction, make sure we always commit
        group_name, robot_name = (request.form[key] for key in PUBLIC_FIELDS)
        image = request.files.get('upload')
        if image:
            if not os.path.isdir(image_upload_path):
                os.makedirs(image_upload_path)
            
            image.save(os.path.join(image_upload_path, image.filename))

        rowid = create(database, group_name, robot_name, image.filename) # ;) let's see if you can figure it out...
    except Exception as error:
        return redirect(url_for('index', error=error))
    finally:
        database.commit()

    return redirect(url_for('.view_team', rowid=rowid))


@routes.post('/modify')
def modify_team():
    database = database_connection(current_app)
    rowid = request.form['id']

    try:
        group_name, robot_name = (request.form.get(key) for key in PUBLIC_FIELDS)
        if group_name:
            modify_group_name(database, rowid, group_name)
        if robot_name:
            modify_robot_name(database, rowid, robot_name)
    except Exception as error:
        return redirect(url_for('index', error=error))
    finally:
        database.commit()

    return redirect(url_for('index'))


@routes.post('/remove')
def remove_team():
    database = database_connection(current_app)
    
    try:
        remove(database, request.form['id'])
    except Exception as error:
        return redirect(url_for('index', error=error))
    finally:
        database.commit()

    return redirect(url_for('index'))