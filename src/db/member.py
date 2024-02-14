import sqlite3
import random


colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']


def create(database: sqlite3.Connection, team_id: int, name: str, color: str) -> int:
    if not color:
        color = random.choice(color)
    result = database.execute('INSERT INTO member (name, color, teamid) VALUES (?, ?, ?) RETURNING rowid', (name, color, team_id))
    return result.fetchone()['rowid']