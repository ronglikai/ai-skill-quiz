"""
AI Skill 知识测试与学习系统
团队内部使用 - 主应用
"""

import os
import asyncio
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
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

db.init_db()


# ==================== 后台评估任务 ====================

async def _bg_evaluate(answer_id: int, question: str, key_points: list, reference_answer: str, user_answer: str):
    """后台评估单题"""
    result = await ai_service.evaluate_answer(question, key_points, reference_answer, user_answer)
    db.update_answer_eval(
        answer_id=answer_id,
        score=result["score"],
        is_correct=result["is_correct"],
        feedback=result["feedback"],
        concept_gaps=result.get("concept_gaps", []),
    )


def _run_bg_eval(answer_id, question, key_points, reference_answer, user_answer):
    """在事件循环中运行后台评估"""
    loop = asyncio.get_event_loop()
    loop.create_task(_bg_evaluate(answer_id, question, key_points, reference_answer, user_answer))


# ==================== 页面路由 ====================

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(name: str = Form(...)):
    name = name.strip()
    if not name:
        return RedirectResponse("/", status_code=303)
    user = db.get_or_create_user(name)
    return RedirectResponse(f"/dashboard?user_id={user['id']}", status_code=303)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: int):
    conn = db.get_db()
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return RedirectResponse("/", status_code=303)
    sessions = db.get_user_sessions(user_id)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": dict(user),
        "sessions": sessions,
        "total_questions": qbank.get_total_count(),
    })


@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request, user_id: int):
    conn = db.get_db()
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return RedirectResponse("/", status_code=303)
    session_id = db.create_session(user_id, qbank.get_total_count())
    return templates.TemplateResponse("test.html", {
        "request": request,
        "user": dict(user),
        "session_id": session_id,
        "questions": qbank.get_all_questions(),
        "total_questions": qbank.get_total_count(),
    })


@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request, session_id: int, user_id: int):
    session = db.get_session(session_id)
    if not session:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "session": session,
        "session_id": session_id,
        "user_id": user_id,
    })


@app.get("/learn", response_class=HTMLResponse)
async def learn_page(request: Request, session_id: int, user_id: int):
    session = db.get_session(session_id)
    if not session:
        return RedirectResponse("/", status_code=303)
    # 获取答题数据，附上题目信息
    answers = db.get_session_answers(session_id)
    enriched = []
    for ans in answers:
        q = qbank.get_question_by_id(ans["question_id"])
        if q:
            enriched.append({
                "question_id": ans["question_id"],
                "question": q["question"],
                "reference_answer": q["reference_answer"],
                "category": q["category"],
                "user_answer": ans["user_answer"],
                "score": ans.get("score", 0) or 0,
                "is_correct": ans.get("is_correct", False),
                "feedback": ans.get("ai_feedback", ""),
                "concept_gaps": ans.get("concept_gaps", []),
            })
    learned_ids = db.get_learned_question_ids(session_id)
    return templates.TemplateResponse("learn.html", {
        "request": request,
        "session": session,
        "session_id": session_id,
        "user_id": user_id,
        "answers_json": enriched,
        "learned_ids": learned_ids,
    })


@app.get("/records", response_class=HTMLResponse)
async def records_page(request: Request, user_id: int = None):
    all_records = db.get_all_records()
    user_detail = db.get_user_detail_records(user_id) if user_id else None
    return templates.TemplateResponse("records.html", {
        "request": request,
        "all_records": all_records,
        "user_detail": user_detail,
        "current_user_id": user_id,
    })


@app.get("/session/{session_id}/detail", response_class=HTMLResponse)
async def session_detail_page(request: Request, session_id: int, user_id: int = None):
    answers = db.get_session_answers(session_id)
    session = db.get_session(session_id)
    if not session:
        return RedirectResponse("/records", status_code=303)
    enriched = []
    for ans in answers:
        q = qbank.get_question_by_id(ans["question_id"])
        enriched.append({**ans, "question_text": q["question"] if q else "未知", "category": q["category"] if q else ""})
    comp = db.get_comprehensive(session_id)
    return templates.TemplateResponse("session_detail.html", {
        "request": request,
        "session": session,
        "answers": enriched,
        "comprehensive": comp,
        "current_user_id": user_id,
    })


# ==================== API 路由 ====================

@app.post("/api/submit-quick")
async def submit_quick(request: Request):
    """快速保存答案，立即返回，后台异步评估"""
    body = await request.json()
    session_id = body.get("session_id")
    question_id = body.get("question_id")
    user_answer = body.get("answer", "").strip()

    if not all([session_id, question_id, user_answer]):
        return {"status": "error", "message": "缺少参数"}

    q = qbank.get_question_by_id(question_id)
    if not q:
        return {"status": "error", "message": "题目不存在"}

    # 1. 快速保存
    answer_id = db.save_answer_quick(session_id, question_id, user_answer)

    # 2. 后台异步评估（不阻塞响应）
    asyncio.get_event_loop().create_task(
        _bg_evaluate(answer_id, q["question"], q["key_points"], q["reference_answer"], user_answer)
    )

    return {"status": "ok", "answer_id": answer_id}


@app.get("/api/session/{session_id}/eval-status")
async def eval_status(session_id: int):
    """查询评估进度"""
    status = db.get_session_eval_status(session_id)
    return {
        "total": status["total"],
        "done": status["done"],
        "all_done": status["total"] > 0 and status["done"] == status["total"],
    }


@app.post("/api/session/{session_id}/comprehensive")
async def generate_comprehensive(session_id: int):
    """生成综合分析"""
    # 检查是否已有分析
    existing = db.get_comprehensive(session_id)
    if existing:
        return {"status": "ok", "data": existing}

    # 收集所有答题数据
    answers = db.get_session_answers(session_id)
    qa_list = []
    for ans in answers:
        q = qbank.get_question_by_id(ans["question_id"])
        if q:
            qa_list.append({
                "question": q["question"],
                "category": q["category"],
                "user_answer": ans["user_answer"],
                "score": ans.get("score", 0) or 0,
                "feedback": ans.get("ai_feedback", ""),
                "concept_gaps": ans.get("concept_gaps", []),
            })

    # 调用综合分析
    result = await ai_service.comprehensive_analysis(qa_list)

    # 更新session分数
    db.complete_session(session_id)
    db.update_session_score(session_id)

    # 保存综合分析
    db.save_comprehensive(session_id, result)

    return {"status": "ok", "data": result}


@app.get("/api/session/{session_id}/comprehensive")
async def get_comprehensive(session_id: int):
    """获取综合分析"""
    data = db.get_comprehensive(session_id)
    if data:
        return {"status": "ok", "data": data}
    return {"status": "not_ready"}


@app.get("/api/session/{session_id}/answers")
async def get_answers(session_id: int):
    """获取答题详情"""
    answers = db.get_session_answers(session_id)
    enriched = []
    for ans in answers:
        q = qbank.get_question_by_id(ans["question_id"])
        enriched.append({
            "question_id": ans["question_id"],
            "question": q["question"] if q else "",
            "category": q["category"] if q else "",
            "user_answer": ans["user_answer"],
            "score": ans.get("score"),
            "is_correct": ans.get("is_correct"),
            "feedback": ans.get("ai_feedback", ""),
            "concept_gaps": ans.get("concept_gaps", []),
        })
    return {"answers": enriched}


@app.post("/api/learn/init")
async def learn_init(request: Request):
    """逐题学习：AI分析回答并提出延伸追问"""
    body = await request.json()
    question = body.get("question", "")
    reference_answer = body.get("reference_answer", "")
    user_answer = body.get("user_answer", "")
    score = body.get("score", 0)
    feedback = body.get("feedback", "")
    concept_gaps = body.get("concept_gaps", [])

    reply = await ai_service.question_learning_init(
        question=question,
        reference_answer=reference_answer,
        user_answer=user_answer,
        score=score,
        feedback=feedback,
        concept_gaps=concept_gaps,
    )

    return {"reply": reply}


@app.post("/api/learn/evaluate")
async def learn_evaluate(request: Request):
    """逐题学习：评估学员对延伸追问的回答"""
    body = await request.json()
    question = body.get("question", "")
    reference_answer = body.get("reference_answer", "")
    followup_question = body.get("followup_question", "")
    user_reply = body.get("user_reply", "").strip()
    chat_history = body.get("chat_history", [])

    if not user_reply:
        return {"passed": False, "reply": "请输入你的回答。"}

    result = await ai_service.question_learning_evaluate(
        question=question,
        reference_answer=reference_answer,
        followup_question=followup_question,
        user_reply=user_reply,
        chat_history=chat_history,
    )

    return result


@app.post("/api/learn/mark-learned")
async def mark_learned(request: Request):
    """标记某道错题已在学习模式中通过"""
    body = await request.json()
    session_id = body.get("session_id")
    question_id = body.get("question_id")

    if not session_id or not question_id:
        return {"status": "error", "message": "缺少参数"}

    db.mark_answer_learned(session_id, question_id)
    all_done = db.check_learning_completion(session_id)
    return {"ok": True, "all_done": all_done}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
