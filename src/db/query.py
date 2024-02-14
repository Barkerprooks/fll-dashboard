import sqlite3
from datetime import datetime

from src.db.run import llsp3_file_format


def nav(database: sqlite3.Connection):
    content = {}
    results = database.execute("SELECT rowid, group_name, robot_name, image FROM team").fetchall()
    for row in results:
        rowid = str(row['rowid'])
        content[rowid] = {
            "robot": row['robot_name'],
            "name": row['group_name'],
            "image": row['image'],
            "runs": runs(database, rowid),
            "members": database.execute("SELECT * FROM member WHERE teamid = ?", (rowid, )).fetchall()
        }
    return content


def runs(database: sqlite3.Connection, team_id: int) -> dict:
    
    content = {}
    results = database.execute(
        '''
        SELECT 
            run.rowid, *
        FROM run
        LEFT JOIN team ON team.rowid = teamid
        WHERE teamid = ?
        ORDER BY robot_slot
        ''', 
        (team_id, )
    ).fetchall()

    for row in results:
        rowid, title, version, group_name = (row[key] for key in ('rowid', 'title', 'version', 'group_name'))
        content[rowid] = {
            'title': title,
            'robot_slot': row['robot_slot'],
            'version': version,
            'created': datetime.fromtimestamp(int(row['created'])).strftime('%c'),
            "updated": datetime.fromtimestamp(int(row['updated'])).strftime('%c'),
            'url': f'llsp3/{group_name}/{llsp3_file_format(group_name, title, version)}'
        }

    return content