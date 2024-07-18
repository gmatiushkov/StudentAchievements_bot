import sqlite3
from models import Achievement, User


def init_db():
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    # Create achievements table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        files TEXT,
        status TEXT NOT NULL DEFAULT 'На рассмотрении',
        student_group TEXT NOT NULL,
        student_name TEXT NOT NULL
    )
    ''')

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        group_number TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


def add_achievement(description, files, student_group, student_name):
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    files_str = ','.join([f"{ft}:{fid}" for ft, fid in files])
    cursor.execute('INSERT INTO achievements (description, files, status, student_group, student_name) VALUES (?, ?, ?, ?, ?)',
                   (description, files_str, 'На рассмотрении', student_group, student_name))
    conn.commit()
    conn.close()


def delete_achievement(achievement_id):
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM achievements WHERE id = ?', (achievement_id,))
    conn.commit()
    conn.close()


def get_achievements():
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, description, files, status, student_group, student_name FROM achievements WHERE status = "Подтверждено"')
    rows = cursor.fetchall()
    conn.close()
    return [Achievement.from_row(row) for row in rows]

def get_pending_achievements():
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, description, files, status, student_group, student_name FROM achievements WHERE status = "На рассмотрении"')
    rows = cursor.fetchall()
    conn.close()
    return [Achievement.from_row(row) for row in rows]


def update_achievement_status(achievement_id, status):
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE achievements SET status = ? WHERE id = ?', (status, achievement_id))
    conn.commit()
    conn.close()


def add_user(full_name, group_number, password):
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (full_name, group_number, password) VALUES (?, ?, ?)', (full_name, group_number, password))
    conn.commit()
    conn.close()

def get_user(full_name, password):
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE full_name = ? AND password = ?', (full_name, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        return User.from_row(row)
    return None
