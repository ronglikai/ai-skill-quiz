"""
AI Skill 知识测试与学习系统
团队内部使用 - 主应用
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

import database as db
import questions as qbank
import ai_service

app = FastAPI(title="AI Skill 知识测试系统")

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# 初始化数据库
db.init_db()


# ==================== 页面路由 ====================

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """登录页"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(name: str = Form(...)):
    """处理登录"""
    name = name.strip()
    if not name:
        return RedirectResponse("/", status_code=303)
    user = db.get_or_create_user(name)
    return RedirectResponse(f"/dashboard?user_id={user['id']}", status_code=303)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: int):
    """仪表盘页面"""
    conn = db.get_db()
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return RedirectResponse("/", status_code=303)

    sessions = db.get_user_sessions(user_id)
    total_questions = qbank.get_total_count()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": dict(user),
        "sessions": sessions,
        "total_questions": total_questions,
    })


@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request, user_id: int, session_id: int = None):
    """测试页面"""
    conn = db.get_db()
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return RedirectResponse("/", status_code=303)

    # 创建新session或继续已有session
    if not session_id:
        session_id = db.create_session(user_id, qbank.get_total_count())

    all_questions = qbank.get_all_questions()
    categories = qbank.get_categories()

    return templates.TemplateResponse("test.html", {
        "request": request,
        "user": dict(user),
        "session_id": session_id,
        "questions": all_questions,
        "categories": categories,
        "total_questions": qbank.get_total_count(),
    })


@app.get("/records", response_class=HTMLResponse)
async def records_page(request: Request, user_id: int = None):
    """记录管理页面"""
    all_records = db.get_all_records()
    # 如果指定了user_id，获取该用户的详细记录
    user_detail = None
    if user_id:
        user_detail = db.get_user_detail_records(user_id)

    return templates.TemplateResponse("records.html", {
        "request": request,
        "all_records": all_records,
        "user_detail": user_detail,
        "current_user_id": user_id,
    })


@app.get("/session/{session_id}/detail", response_class=HTMLResponse)
async def session_detail_page(request: Request, session_id: int, user_id: int = None):
    """某次测试的详细记录"""
    answers = db.get_session_answers(session_id)

    # 获取session信息
    conn = db.get_db()
    cursor = conn.execute(
        """SELECT ts.*, u.name as user_name FROM test_sessions ts
           JOIN users u ON ts.user_id = u.id WHERE ts.id = ?""",
        (session_id,),
    )
    session = cursor.fetchone()
    conn.close()
    if not session:
        return RedirectResponse("/records", status_code=303)

    # 为每个answer附加题目信息
    enriched_answers = []
    for ans in answers:
        q = qbank.get_question_by_id(ans["question_id"])
        enriched_answers.append({**ans, "question_text": q["question"] if q else "未知题目", "category": q["category"] if q else ""})

    return templates.TemplateResponse("session_detail.html", {
        "request": request,
        "session": dict(session),
        "answers": enriched_answers,
        "current_user_id": user_id,
    })


# ==================== API 路由 ====================

@app.get("/api/question/{question_id}")
async def get_question(question_id: int):
    """获取题目（不含答案）"""
    q = qbank.get_question_by_id(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="题目不存在")
    return {
        "id": q["id"],
        "category": q["category"],
        "difficulty": q["difficulty"],
        "question": q["question"],
    }


@app.post("/api/submit")
async def submit_answer(request: Request):
    """提交答案并获取AI评估"""
    body = await request.json()
    session_id = body.get("session_id")
    question_id = body.get("question_id")
    user_answer = body.get("answer", "").strip()

    if not all([session_id, question_id, user_answer]):
        raise HTTPException(status_code=400, detail="缺少必要参数")

    # 获取题目
    q = qbank.get_question_by_id(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="题目不存在")

    # 检查是否已经答对
    if db.has_correct_answer(session_id, question_id):
        return {"status": "already_correct", "message": "你已经答对了这道题！"}

    # 获取尝试次数
    attempt = db.get_question_attempt_count(session_id, question_id) + 1

    # 调用AI评估
    result = await ai_service.evaluate_answer(
        question=q["question"],
        key_points=q["key_points"],
        reference_answer=q["reference_answer"],
        user_answer=user_answer,
    )

    # 保存答题记录
    db.save_answer(
        session_id=session_id,
        question_id=question_id,
        user_answer=user_answer,
        score=result["score"],
        is_correct=result["is_correct"],
        ai_feedback=result["feedback"],
        knowledge_gaps=result["knowledge_gaps"],
        guidance=result["guidance"],
        attempt_number=attempt,
    )

    return {
        "status": "ok",
        "result": result,
        "attempt": attempt,
    }


@app.post("/api/complete-session")
async def complete_session(request: Request):
    """完成测试session"""
    body = await request.json()
    session_id = body.get("session_id")
    if session_id:
        db.complete_session(session_id)
    return {"status": "ok"}


@app.get("/api/session/{session_id}/progress")
async def get_session_progress(session_id: int):
    """获取session答题进度"""
    answers = db.get_session_answers(session_id)
    # 按question_id分组，取最高分
    progress = {}
    for ans in answers:
        qid = ans["question_id"]
        if qid not in progress or ans["score"] > progress[qid]["score"]:
            progress[qid] = {
                "question_id": qid,
                "score": ans["score"],
                "is_correct": ans["is_correct"],
                "attempts": 0,
            }
        progress[qid]["attempts"] += 1

    return {"progress": list(progress.values())}


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
