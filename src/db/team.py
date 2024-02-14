import sqlite3


PUBLIC_FIELDS = ('group_name', 'robot_name')


def create(database: sqlite3.Connection, group_name: str, robot_name: str, image: str):
    result = database.execute('INSERT INTO team (group_name, robot_name, image) VALUES (?, ?, ?) RETURNING rowid', (group_name, robot_name, image))
    return result.fetchone()['rowid'] # fetchone is still a tuple, or a ROW, so get the first element out of it


def modify_group_name(database: sqlite3.Connection, rowid: int, group_name: str):
    database.execute("UPDATE team SET group_name = ? WHERE rowid = ?", (group_name, rowid))


def modify_robot_name(database: sqlite3.Connection, rowid: int, robot_name: str):
    database.execute("UPDATE team SET robot_name = ? WHERE rowid = ?", (robot_name, rowid))


def remove(database: sqlite3.Connection, rowid: int):
    database.execute("DELETE FROM team WHERE rowid = ?", (rowid, ))


def get(database: sqlite3.Connection, rowid: int):
    return database.execute("SELECT rowid, * FROM team WHERE rowid = ?", (rowid, )).fetchone()