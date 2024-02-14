from flask import Flask, request, redirect, url_for, render_template
from src.db.config import database_connection, initialize_database
from src.db.query import nav

from src.routes import run, team, member
import json

app = Flask(__name__) # handles it all
app.config.from_file('./etc/config.json', load=json.load)

# create the tables if they dont exist
with app.app_context():
    initialize_database(app)


app.register_blueprint(member.routes)
app.register_blueprint(team.routes)
app.register_blueprint(run.routes)


@app.get('/') # index = home page
def index():
    database = database_connection(app)

    return render_template(
        'index.html', 
        page='Dashboard',
        nav=nav(database),
        version=app.config['VERSION'], 
        error=request.args.get('error'),
        modal=request.args.get('modal'),
        edit=request.args.get('edit')
    )