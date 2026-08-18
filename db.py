import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "minutesbot.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            owner TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Open',
            planner_task_id TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def insert_task(description, owner, due_date, planner_task_id):
    conn = get_conn()
    conn.execute(
        "INSERT INTO tasks (description, owner, due_date, planner_task_id) VALUES (?, ?, ?, ?)",
        (description, owner, due_date, planner_task_id),
    )
    conn.commit()
    conn.close()


def get_all_tasks():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_task_status(task_id, status):
    conn = get_conn()
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()
