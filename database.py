import sqlite3
from models import Achievement


def init_db():
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        files TEXT,
        status TEXT NOT NULL DEFAULT 'На рассмотрении'
    )
    ''')

    # Add 'status' column if it doesn't exist
    cursor.execute("PRAGMA table_info(achievements)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'status' not in columns:
        cursor.execute("ALTER TABLE achievements ADD COLUMN status TEXT NOT NULL DEFAULT 'На рассмотрении'")

    conn.commit()
    conn.close()


def add_achievement(description, files):
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    files_str = ','.join([f"{ft}:{fid}" for ft, fid in files])
    cursor.execute('INSERT INTO achievements (description, files, status) VALUES (?, ?, ?)',
                   (description, files_str, 'На рассмотрении'))
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
    cursor.execute('SELECT id, description, files, status FROM achievements WHERE status = "Подтверждено"')
    rows = cursor.fetchall()
    conn.close()
    return [Achievement.from_row(row) for row in rows]


def get_pending_achievements():
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, description, files, status FROM achievements WHERE status = "На рассмотрении"')
    rows = cursor.fetchall()
    conn.close()
    return [Achievement.from_row(row) for row in rows]


def update_achievement_status(achievement_id, status):
    conn = sqlite3.connect('achievements.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE achievements SET status = ? WHERE id = ?', (status, achievement_id))
    conn.commit()
    conn.close()
