"""
AI评估服务 - 使用Kimi k2.5模型
重点：评估概念理解深度，而非死记硬背
"""

import json
import os
import httpx

KIMI_API_KEY = os.environ.get("KIMI_API_KEY", "sk-P8kJiGgSU32op9pfbBWUhFt7Q20TCjU7y3tUWoYIT2IDOZwz")
KIMI_BASE_URL = os.environ.get("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
KIMI_MODEL = os.environ.get("KIMI_MODEL", "kimi-latest")


def _get_proxy():
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    if http_proxy and not http_proxy.startswith("socks"):
        return http_proxy
    return None


async def _call_kimi(messages: list, temperature: float = 0.3) -> str:
    """统一的Kimi API调用"""
    async with httpx.AsyncClient(timeout=90.0, proxy=_get_proxy()) as client:
        response = await client.post(
            f"{KIMI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {KIMI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": KIMI_MODEL,
                "messages": messages,
                "temperature": temperature,
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


def _parse_json(content: str) -> dict:
    """解析可能被markdown包裹的JSON"""
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        content = "\n".join(lines[1:end]).strip()
    return json.loads(content)


# ==================== 单题评估（概念理解导向） ====================

async def evaluate_answer(question: str, key_points: list, reference_answer: str, user_answer: str) -> dict:
    """
    评估单题回答——聚焦概念理解而非背诵
    """
    key_points_text = "\n".join(f"- {p}" for p in key_points)

    system_prompt = """你是一位AI教育评估专家。你的任务是评估学员是否**真正理解**了某个概念，而不是检查他们是否记住了文档原文。

核心评估原则：
1. **评估理解，而非背诵**——即使用词完全不同，只要概念本质理解正确就应高分认可
2. **接受多元表达**——用类比、例子、自己的话表达同一概念，甚至比原文更好
3. **关注"为什么"而非"是什么"**——能解释原因和逻辑关系的回答，优于罗列事实的回答
4. **区分核心vs细节**——核心概念理解才是关键，具体字段名、步骤编号等细节遗漏不重要
5. **鼓励思考深度**——如果学员的回答展现了超出参考答案的独立思考，应加分

评分维度和权重：
- 概念本质理解（50%）：是否抓住了核心"为什么"和"是什么"
- 逻辑关联能力（25%）：能否将概念与其他概念、实际场景联系起来
- 表达完整性（25%）：核心方面是否有明显遗漏（注意：细节遗漏不扣分）

评分标准：
- 80-100：理解准确，能用自己的话清晰表达核心概念
- 60-79：基本理解，但有些地方理解不够深入
- 40-59：部分理解，存在概念混淆或理解偏差
- 0-39：未理解核心概念，或存在根本性的概念错误

你必须返回严格JSON（无markdown代码块包裹）：
{
  "score": 0-100,
  "is_correct": true/false（60分以上算correct）,
  "feedback": "简要评价（1-2句话）",
  "concept_gaps": ["未理解的核心概念1", "核心概念2"]
}"""

    user_prompt = f"""题目：{question}

核心概念要点（仅供你参考理解题目考察方向，不是评判标准）：
{key_points_text}

参考答案（仅供你理解正确概念，不要求学员原文复述）：
{reference_answer}

学员回答：
{user_answer}

请评估这位学员是否真正理解了这个概念。记住：不同的措辞、类比、例子都是有效的，关键是概念本质是否正确。"""

    try:
        content = await _call_kimi([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])
        result = _parse_json(content)
        return {
            "score": result.get("score", 0),
            "is_correct": result.get("is_correct", False),
            "feedback": result.get("feedback", ""),
            "concept_gaps": result.get("concept_gaps", []),
        }
    except Exception as e:
        return {
            "score": -1,
            "is_correct": False,
            "feedback": f"评估异常：{str(e)[:200]}",
            "concept_gaps": [],
        }


# ==================== 综合分析（全部答完后） ====================

async def comprehensive_analysis(questions_and_answers: list) -> dict:
    """
    综合分析20道题的整体表现
    questions_and_answers: [{"question": ..., "category": ..., "user_answer": ..., "score": ..., "feedback": ..., "concept_gaps": [...]}, ...]
    """
    qa_text = ""
    for i, qa in enumerate(questions_and_answers, 1):
        qa_text += f"""
---第{i}题 [{qa['category']}]---
题目：{qa['question']}
回答：{qa['user_answer']}
得分：{qa['score']}
评价：{qa['feedback']}
概念盲点：{', '.join(qa.get('concept_gaps', [])) or '无'}
"""

    system_prompt = """你是一位资深AI教育顾问。请对学员的整体AI知识测试表现进行深度综合分析。

分析要求：
1. 不要简单重复每道题的反馈——要做跨题目的综合洞察
2. 识别理解模式（比如："概念理解强但实操细节弱"、"能理解单个概念但不善于关联"）
3. 区分"知道但表达不清"和"根本不理解"
4. 给出具体可操作的学习路径，不要泛泛而谈

你必须返回严格JSON（无markdown代码块包裹）：
{
  "overall_score": 0-100的整数,
  "level": "精通/良好/基础/需提升" 四选一,
  "summary": "2-3句总结，言简意赅",
  "strong_areas": [{"area": "领域名", "detail": "具体表现"}],
  "weak_areas": [{"area": "领域名", "detail": "具体问题", "suggestion": "怎么补"}],
  "patterns": ["跨题目的理解模式/特点"],
  "learning_path": [{"step": 1, "action": "做什么", "focus": "重点是什么"}]
}"""

    user_prompt = f"""以下是学员完成的全部20道AI Skill知识测试：
{qa_text}

请进行综合深度分析。"""

    try:
        content = await _call_kimi([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ], temperature=0.4)
        return _parse_json(content)
    except Exception as e:
        return {
            "overall_score": 0,
            "level": "需提升",
            "summary": f"分析生成失败：{str(e)[:200]}",
            "strong_areas": [],
            "weak_areas": [],
            "patterns": [],
            "learning_path": [],
        }


# ==================== 对话式学习引导 ====================

async def chat_response(user_name: str, weak_areas: list, strong_areas: list, summary: str, chat_history: list, user_message: str) -> str:
    """
    苏格拉底式对话教学
    chat_history: [{"role": "assistant"/"user", "content": "..."}]
    """
    weak_text = "\n".join(f"- {w['area']}：{w['detail']}" for w in weak_areas) if weak_areas else "暂无明显薄弱点"
    strong_text = "\n".join(f"- {s['area']}" for s in strong_areas) if strong_areas else "暂无"

    system_prompt = f"""你是一位耐心的AI技能教学导师，正在和{user_name}进行一对一学习辅导。

学员背景：
- 测试总结：{summary}
- 已掌握：{strong_text}
- 需加强：{weak_text}

教学方法——苏格拉底对话法：
1. **不要直接给答案**——通过提问引导学员自己发现和思考
2. **从已知搭到未知**——从学员已掌握的概念出发，搭桥到新概念
3. **多用类比**——用日常生活的例子解释抽象的技术概念
4. **一次一个点**——每次只聚焦一个知识点，确认理解后再下一个
5. **积极鼓励**——肯定进步，对错误温和纠正

对话风格：
- 简洁友好，每次回复不超过150字
- 适当用反问引导思考
- 遇到正确理解时明确肯定并深化
- 遇到误解时不直接否定，而是追问让学员自己发现矛盾

如果是第一条消息（对话刚开始），请简要介绍自己，说明学员的薄弱领域，然后从最需要加强的一个概念开始提问引导。"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})

    try:
        return await _call_kimi(messages, temperature=0.6)
    except Exception as e:
        return f"抱歉，对话服务暂时出错了：{str(e)[:100]}。请重试。"
