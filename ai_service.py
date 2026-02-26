"""
AI评估服务 - 使用Kimi k2.5模型评估用户回答
"""

import json
import os
import httpx

KIMI_API_KEY = os.environ.get("KIMI_API_KEY", "sk-P8kJiGgSU32op9pfbBWUhFt7Q20TCjU7y3tUWoYIT2IDOZwz")
KIMI_BASE_URL = os.environ.get("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
KIMI_MODEL = os.environ.get("KIMI_MODEL", "kimi-latest")


async def evaluate_answer(question: str, key_points: list, reference_answer: str, user_answer: str) -> dict:
    """
    调用Kimi API评估用户的回答
    返回: {"is_correct": bool, "score": int, "feedback": str, "knowledge_gaps": list, "guidance": str}
    """
    key_points_text = "\n".join(f"- {p}" for p in key_points)

    system_prompt = """你是一个AI技能教学评估系统，专门评估团队成员对AI工具知识的掌握程度。
你的评估风格应该是：
1. 友善但严格——不要轻易给高分，但也不要打击学习积极性
2. 具体指出问题——不要笼统说"不够准确"，要指出具体哪个知识点有误或遗漏
3. 引导式反馈——不要直接告诉答案，而是引导用户思考正确方向
4. 中文回复

评分标准：
- 80-100分：核心知识点全部覆盖且理解准确，表述清晰
- 60-79分：覆盖了主要知识点，但有些理解不够深入或有遗漏
- 40-59分：只答出部分知识点，存在明显的理解偏差
- 0-39分：大部分知识点未覆盖，或存在严重的概念错误

你必须返回严格的JSON格式（不要包含markdown代码块标记），包含以下字段：
{
  "is_correct": true或false（60分以上算correct）,
  "score": 0到100的整数,
  "feedback": "对用户回答的具体评价，指出哪些点答得好、哪些点有问题",
  "knowledge_gaps": ["知识盲点1", "知识盲点2"],
  "guidance": "针对性的学习引导，帮助用户理解正确概念（如果回答正确则给予鼓励和补充）"
}"""

    user_prompt = f"""请评估以下回答：

**题目**：{question}

**核心知识点**（评估依据）：
{key_points_text}

**参考答案**：
{reference_answer}

**用户回答**：
{user_answer}

请根据核心知识点评估用户回答的准确性和完整性，返回JSON格式的评估结果。"""

    try:
        # 使用HTTP代理（如果有的话，跳过SOCKS代理）
        http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
        socks_proxy = os.environ.get("ALL_PROXY") or os.environ.get("all_proxy")
        # 仅在有HTTP代理且非SOCKS时使用，否则不走代理
        proxy = http_proxy if (http_proxy and not http_proxy.startswith("socks")) else None
        async with httpx.AsyncClient(timeout=60.0, proxy=proxy) as client:
            response = await client.post(
                f"{KIMI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {KIMI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": KIMI_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.3,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            # 尝试解析JSON，处理可能的markdown代码块包裹
            content = content.strip()
            if content.startswith("```"):
                # 去掉代码块标记
                lines = content.split("\n")
                content = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
                content = content.strip()

            result = json.loads(content)

            # 确保所有必需字段存在
            return {
                "is_correct": result.get("is_correct", False),
                "score": result.get("score", 0),
                "feedback": result.get("feedback", "评估完成"),
                "knowledge_gaps": result.get("knowledge_gaps", []),
                "guidance": result.get("guidance", ""),
            }

    except httpx.HTTPStatusError as e:
        return {
            "is_correct": False,
            "score": -1,
            "feedback": f"AI服务调用失败（HTTP {e.response.status_code}），请稍后重试。",
            "knowledge_gaps": [],
            "guidance": "系统暂时无法评估，请稍后再试。",
        }
    except json.JSONDecodeError:
        # AI返回了非JSON格式，尝试提取有用信息
        return {
            "is_correct": False,
            "score": -1,
            "feedback": f"AI返回格式异常，原始回复：{content[:500]}",
            "knowledge_gaps": [],
            "guidance": "系统评估格式异常，请稍后再试。",
        }
    except Exception as e:
        return {
            "is_correct": False,
            "score": -1,
            "feedback": f"系统错误：{str(e)}",
            "knowledge_gaps": [],
            "guidance": "系统暂时出现问题，请稍后再试。",
        }
