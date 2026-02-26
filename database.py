"""
数据库操作模块 - SQLite
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "quiz.db"


def get_db():
    """获取数据库连接"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """初始化数据库表"""
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
            score INTEGER NOT NULL DEFAULT 0,
            is_correct INTEGER NOT NULL DEFAULT 0,
            ai_feedback TEXT,
            knowledge_gaps TEXT,
            guidance TEXT,
            attempt_number INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (session_id) REFERENCES test_sessions(id)
        );
    """)
    conn.commit()
    conn.close()


def get_or_create_user(name: str) -> dict:
    """获取或创建用户"""
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


def create_session(user_id: int, total_questions: int) -> int:
    """创建测试会话，返回session_id"""
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO test_sessions (user_id, total_questions) VALUES (?, ?)",
        (user_id, total_questions),
    )
    conn.commit()
    session_id = cursor.lastrowid
    conn.close()
    return session_id


def save_answer(session_id: int, question_id: int, user_answer: str, score: int, is_correct: bool, ai_feedback: str, knowledge_gaps: list, guidance: str, attempt_number: int):
    """保存用户的答题记录"""
    conn = get_db()
    conn.execute(
        """INSERT INTO answers (session_id, question_id, user_answer, score, is_correct, ai_feedback, knowledge_gaps, guidance, attempt_number)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (session_id, question_id, user_answer, score, int(is_correct), ai_feedback, json.dumps(knowledge_gaps, ensure_ascii=False), guidance, attempt_number),
    )
    # 更新session的正确数
    if is_correct:
        conn.execute(
            "UPDATE test_sessions SET correct_count = correct_count + 1 WHERE id = ?",
            (session_id,),
        )
    conn.commit()
    conn.close()


def complete_session(session_id: int):
    """完成测试会话"""
    conn = get_db()
    conn.execute(
        "UPDATE test_sessions SET completed_at = datetime('now', 'localtime') WHERE id = ?",
        (session_id,),
    )
    conn.commit()
    conn.close()


def get_user_sessions(user_id: int) -> list:
    """获取用户的所有测试记录"""
    conn = get_db()
    cursor = conn.execute(
        """SELECT ts.*, u.name as user_name
           FROM test_sessions ts
           JOIN users u ON ts.user_id = u.id
           WHERE ts.user_id = ?
           ORDER BY ts.started_at DESC""",
        (user_id,),
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_session_answers(session_id: int) -> list:
    """获取某次测试的所有答题记录"""
    conn = get_db()
    cursor = conn.execute(
        """SELECT * FROM answers
           WHERE session_id = ?
           ORDER BY question_id, attempt_number""",
        (session_id,),
    )
    rows = [dict(r) for r in cursor.fetchall()]
    for row in rows:
        if row.get("knowledge_gaps"):
            try:
                row["knowledge_gaps"] = json.loads(row["knowledge_gaps"])
            except (json.JSONDecodeError, TypeError):
                row["knowledge_gaps"] = []
    conn.close()
    return rows


def get_all_records() -> list:
    """获取所有用户的测试概况"""
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


def get_user_detail_records(user_id: int) -> dict:
    """获取用户的详细测试历史"""
    conn = get_db()

    # 用户信息
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    user = dict(row) if row else None

    # 所有session
    cursor = conn.execute(
        """SELECT ts.*,
                  (SELECT COUNT(DISTINCT question_id) FROM answers WHERE session_id = ts.id AND is_correct = 1) as unique_correct
           FROM test_sessions ts
           WHERE ts.user_id = ?
           ORDER BY ts.started_at DESC""",
        (user_id,),
    )
    sessions = [dict(r) for r in cursor.fetchall()]

    # 每道题的最佳成绩
    cursor = conn.execute(
        """SELECT a.question_id, MAX(a.score) as best_score, MAX(a.is_correct) as ever_correct,
                  COUNT(*) as total_attempts
           FROM answers a
           JOIN test_sessions ts ON a.session_id = ts.id
           WHERE ts.user_id = ?
           GROUP BY a.question_id""",
        (user_id,),
    )
    question_stats = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return {
        "user": user,
        "sessions": sessions,
        "question_stats": question_stats,
    }


def get_question_attempt_count(session_id: int, question_id: int) -> int:
    """获取某个session中某道题的尝试次数"""
    conn = get_db()
    cursor = conn.execute(
        "SELECT COUNT(*) as cnt FROM answers WHERE session_id = ? AND question_id = ?",
        (session_id, question_id),
    )
    result = cursor.fetchone()
    conn.close()
    return result["cnt"] if result else 0


def has_correct_answer(session_id: int, question_id: int) -> bool:
    """检查某道题是否已经回答正确"""
    conn = get_db()
    cursor = conn.execute(
        "SELECT COUNT(*) as cnt FROM answers WHERE session_id = ? AND question_id = ? AND is_correct = 1",
        (session_id, question_id),
    )
    result = cursor.fetchone()
    conn.close()
    return result["cnt"] > 0 if result else False
