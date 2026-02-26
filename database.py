"""
数据库操作模块 - SQLite
"""

import os
import sqlite3
import json
from pathlib import Path

_db_dir = os.environ.get("DATA_DIR", str(Path(__file__).parent / "data"))
DB_PATH = Path(_db_dir) / "quiz.db"


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS test_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            started_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            completed_at TEXT,
            total_questions INTEGER NOT NULL DEFAULT 0,
            correct_count INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            user_answer TEXT NOT NULL,
            eval_status TEXT NOT NULL DEFAULT 'pending',
            score INTEGER,
            is_correct INTEGER,
            ai_feedback TEXT,
            concept_gaps TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (session_id) REFERENCES test_sessions(id)
        );

        CREATE TABLE IF NOT EXISTS comprehensive_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER UNIQUE NOT NULL,
            overall_score INTEGER,
            level TEXT,
            summary TEXT,
            strong_areas TEXT,
            weak_areas TEXT,
            patterns TEXT,
            learning_path TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (session_id) REFERENCES test_sessions(id)
        );
    """)
    conn.commit()
    conn.close()


# ==================== 用户 ====================

def get_or_create_user(name: str) -> dict:
    conn = get_db()
    cursor = conn.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    if not user:
        conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        cursor = conn.execute("SELECT * FROM users WHERE name = ?", (name,))
        user = cursor.fetchone()
    result = dict(user)
    conn.close()
    return result


# ==================== 会话 ====================

def create_session(user_id: int, total_questions: int) -> int:
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO test_sessions (user_id, total_questions) VALUES (?, ?)",
        (user_id, total_questions),
    )
    conn.commit()
    session_id = cursor.lastrowid
    conn.close()
    return session_id


def complete_session(session_id: int):
    conn = get_db()
    conn.execute(
        "UPDATE test_sessions SET completed_at = datetime('now', 'localtime') WHERE id = ?",
        (session_id,),
    )
    conn.commit()
    conn.close()


def update_session_score(session_id: int):
    """根据answers表重新计算正确数"""
    conn = get_db()
    cursor = conn.execute(
        "SELECT COUNT(*) as cnt FROM answers WHERE session_id = ? AND is_correct = 1",
        (session_id,),
    )
    count = cursor.fetchone()["cnt"]
    conn.execute(
        "UPDATE test_sessions SET correct_count = ? WHERE id = ?",
        (count, session_id),
    )
    conn.commit()
    conn.close()


def get_session(session_id: int) -> dict:
    conn = get_db()
    cursor = conn.execute(
        "SELECT ts.*, u.name as user_name FROM test_sessions ts JOIN users u ON ts.user_id = u.id WHERE ts.id = ?",
        (session_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# ==================== 答题（快速保存 + 后台评估更新） ====================

def save_answer_quick(session_id: int, question_id: int, user_answer: str) -> int:
    """快速保存答案，不等评估，返回answer_id"""
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO answers (session_id, question_id, user_answer, eval_status) VALUES (?, ?, ?, 'pending')",
        (session_id, question_id, user_answer),
    )
    conn.commit()
    answer_id = cursor.lastrowid
    conn.close()
    return answer_id


def update_answer_eval(answer_id: int, score: int, is_correct: bool, feedback: str, concept_gaps: list):
    """后台评估完成后更新"""
    conn = get_db()
    conn.execute(
        """UPDATE answers SET eval_status = 'done', score = ?, is_correct = ?, ai_feedback = ?, concept_gaps = ?
           WHERE id = ?""",
        (score, int(is_correct), feedback, json.dumps(concept_gaps, ensure_ascii=False), answer_id),
    )
    conn.commit()
    conn.close()


def get_session_eval_status(session_id: int) -> dict:
    """获取评估进度"""
    conn = get_db()
    cursor = conn.execute(
        "SELECT COUNT(*) as total, SUM(CASE WHEN eval_status = 'done' THEN 1 ELSE 0 END) as done FROM answers WHERE session_id = ?",
        (session_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return {"total": row["total"] or 0, "done": row["done"] or 0}


def get_session_answers(session_id: int) -> list:
    conn = get_db()
    cursor = conn.execute(
        "SELECT * FROM answers WHERE session_id = ? ORDER BY question_id",
        (session_id,),
    )
    rows = [dict(r) for r in cursor.fetchall()]
    for row in rows:
        if row.get("concept_gaps"):
            try:
                row["concept_gaps"] = json.loads(row["concept_gaps"])
            except (json.JSONDecodeError, TypeError):
                row["concept_gaps"] = []
        else:
            row["concept_gaps"] = []
    conn.close()
    return rows


# ==================== 综合分析 ====================

def save_comprehensive(session_id: int, data: dict):
    conn = get_db()
    conn.execute(
        """INSERT OR REPLACE INTO comprehensive_analyses
           (session_id, overall_score, level, summary, strong_areas, weak_areas, patterns, learning_path)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            session_id,
            data.get("overall_score", 0),
            data.get("level", ""),
            data.get("summary", ""),
            json.dumps(data.get("strong_areas", []), ensure_ascii=False),
            json.dumps(data.get("weak_areas", []), ensure_ascii=False),
            json.dumps(data.get("patterns", []), ensure_ascii=False),
            json.dumps(data.get("learning_path", []), ensure_ascii=False),
        ),
    )
    conn.commit()
    conn.close()


def get_comprehensive(session_id: int):
    conn = get_db()
    cursor = conn.execute("SELECT * FROM comprehensive_analyses WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    for key in ("strong_areas", "weak_areas", "patterns", "learning_path"):
        if d.get(key):
            try:
                d[key] = json.loads(d[key])
            except (json.JSONDecodeError, TypeError):
                d[key] = []
        else:
            d[key] = []
    return d


# ==================== 记录查询 ====================

def get_all_records() -> list:
    conn = get_db()
    cursor = conn.execute(
        """SELECT u.id as user_id, u.name,
                  COUNT(ts.id) as total_sessions,
                  COALESCE(SUM(ts.correct_count), 0) as total_correct,
                  COALESCE(SUM(ts.total_questions), 0) as total_questions,
                  MAX(ts.started_at) as last_test_at
           FROM users u
           LEFT JOIN test_sessions ts ON u.id = ts.user_id
           GROUP BY u.id, u.name
           ORDER BY last_test_at DESC""",
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_user_sessions(user_id: int) -> list:
    conn = get_db()
    cursor = conn.execute(
        "SELECT ts.*, u.name as user_name FROM test_sessions ts JOIN users u ON ts.user_id = u.id WHERE ts.user_id = ? ORDER BY ts.started_at DESC",
        (user_id,),
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_user_detail_records(user_id: int) -> dict:
    conn = get_db()
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    user = dict(row) if row else None

    cursor = conn.execute(
        "SELECT * FROM test_sessions WHERE user_id = ? ORDER BY started_at DESC",
        (user_id,),
    )
    sessions = [dict(r) for r in cursor.fetchall()]

    cursor = conn.execute(
        """SELECT a.question_id, MAX(a.score) as best_score, MAX(a.is_correct) as ever_correct,
                  COUNT(*) as total_attempts
           FROM answers a JOIN test_sessions ts ON a.session_id = ts.id
           WHERE ts.user_id = ? GROUP BY a.question_id""",
        (user_id,),
    )
    question_stats = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"user": user, "sessions": sessions, "question_stats": question_stats}
