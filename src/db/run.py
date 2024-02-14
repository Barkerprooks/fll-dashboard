import sqlite3


def create(database: sqlite3.Connection, team_id: int, robot_slot: int, title: str) -> int:
    result = database.execute('INSERT INTO run (teamid, robot_slot, title) VALUES (?, ?, ?) RETURNING rowid', (team_id, robot_slot, title))
    return result.fetchone()['rowid']


def modify_robot_slot(database: sqlite3.Connection, rowid: int, robot_slot: int):
    database.execute('UPDATE run SET (robot_slot, updated) = (?, CURRENT_TIME) WHERE rowid = ?', (robot_slot, rowid))


def modify_title(database: sqlite3.Connection, rowid: int, title: str):
    database.execute('UPDATE run SET (title, updated) = (?, CURRENT_TIME) WHERE rowid = ?', (title, rowid))


def update_file(database: sqlite3.Connection, rowid: int, version: str):
    database.execute('UPDATE run SET (version, updated) = (?, CURRENT_TIME) WHERE rowid = ?', (version, rowid))


def remove(database: sqlite3.Connection, rowid: int):
    database.execute('DELETE FROM run WHERE rowid = ?', (rowid, ))


def get(database: sqlite3.Connection, rowid: int) -> dict:
    return database.execute('SELECT rowid, * FROM run WHERE rowid = ?', (rowid, )).fetchone()


def llsp3_file_format(group_name: str, title: str, version: str) -> str:
    return f'fll-{group_name}-{title}-{version}.llsp3'