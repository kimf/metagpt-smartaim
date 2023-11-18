## database.py
import sqlite3
import json
from typing import List, Dict, Tuple
import bcrypt

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.scores = []
        self.dispersion_pattern = {}
        self.clubs = []

    def add_score(self, score: int):
        self.scores.append(score)

    def get_scores(self) -> List[int]:
        return self.scores

    def update_dispersion_pattern(self, dispersion_pattern: Dict[str, Tuple[float, float]]):
        self.dispersion_pattern = dispersion_pattern

    def get_dispersion_pattern(self) -> Dict[str, Tuple[float, float]]:
        return self.dispersion_pattern

    def add_club(self, club: str):
        self.clubs.append(club)

    def get_clubs(self) -> List[str]:
        return self.clubs

class Database:
    def __init__(self, db_name: str = 'smartaim_golf.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                clubs TEXT,
                scores TEXT,
                dispersion_pattern TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, user: User):
        clubs = json.dumps(user.get_clubs())
        scores = json.dumps(user.get_scores())
        dispersion_pattern = json.dumps(user.get_dispersion_pattern())
        self.cursor.execute('''
            INSERT INTO users (username, password, clubs, scores, dispersion_pattern)
            VALUES (?, ?, ?, ?, ?)
        ''', (user.username, user.password, clubs, scores, dispersion_pattern))
        self.conn.commit()

    def get_user(self, username: str) -> User:
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        username, password, clubs, scores, dispersion_pattern = row
        user = User(username, password)
        user.clubs = json.loads(clubs)
        user.scores = json.loads(scores)
        user.dispersion_pattern = json.loads(dispersion_pattern)
        return user

    def update_user(self, user: User):
        clubs = json.dumps(user.get_clubs())
        scores = json.dumps(user.get_scores())
        dispersion_pattern = json.dumps(user.get_dispersion_pattern())
        self.cursor.execute('''
            UPDATE users
            SET password = ?, clubs = ?, scores = ?, dispersion_pattern = ?
            WHERE username = ?
        ''', (user.password, clubs, scores, dispersion_pattern, user.username))
        self.conn.commit()

    def delete_user(self, username: str):
        self.cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        self.conn.commit()
