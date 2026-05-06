import httpx
import json

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, MAX_RETRIES, REQUEST_TIMEOUT

SYSTEM_MESSAGE = "你是一个严谨的 AI 产品经理助手，擅长用户研究、需求分析和结构化输出。"


def call_llm(prompt: str, temperature: float = 0.2) -> str:
    if not DEEPSEEK_API_KEY:
        raise ValueError(
            "DEEPSEEK_API_KEY 未配置。请在 .env 文件中设置 DEEPSEEK_API_KEY=sk-your-key"
        )

    url = f"{DEEPSEEK_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
    }

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
                resp = client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            last_error = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
        except httpx.TimeoutException:
            last_error = f"请求超时（{REQUEST_TIMEOUT}s）"
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            last_error = f"响应解析失败: {e}"
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"

    return f"[LLM 调用失败] 重试 {MAX_RETRIES} 次后仍失败: {last_error}"
